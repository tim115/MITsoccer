import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns

# adapted from snippet $435

basePath = '/Users/adrianmuller/Desktop/soccer-analytics-repo/data/' # TODO insert path to the directory with the data
def get_json(file):
    with open(basePath+file, encoding='utf8') as f:
        js = json.load(f)
        return js

save_path = '/Users/adrianmuller/Desktop/soccer-analytics-repo/code/adi_xggraph_plots/' # TODO insert path where you want to save the figures

#load both datasets into dataframes [TODO adapt file names/relative paths]
wyscout = pd.json_normalize(get_json('wyscout/5111384/5111384_events.json')['events'])
statsb = pd.json_normalize(get_json('statsbomb360/events/3788747.json'))

#filter for shots and extract only relevant information into unified format [minute, second, xg, team, isGoal]
shots_wy_r = wyscout[((wyscout['type.primary']=='shot') | (wyscout['type.primary']=='penalty'))]
shots_sb_r = statsb[statsb['type.name']=='Shot']

shots_wy = shots_wy_r[['minute','second','shot.xg','team.name','shot.isGoal']].rename(columns={'shot.xg':'xg', 'team.name':'team', 'shot.isGoal':'isGoal'})

shots_sb_r['isGoal'] = shots_sb_r['shot.outcome.name']=='Goal'
shots_sb = shots_sb_r[['minute','second','shot.statsbomb_xg', 'possession_team.name', 'isGoal']].rename(columns={'shot.statsbomb_xg':'xg', 'possession_team.name':'team'})

#when passed data for one team in format [minute, second, cumXg(cumulated xg), ...] returns dataframe with points that create the 'steps' in the plot
def cleanLines(data, max_):
    '''inserts additional data points to create the steps'''
    n = data.shape[0]
    time = np.zeros(2*n+2, float)
    time[-1] = max_
    time[1:-1:2] = data['minute'] + data['second']/60.
    time[2::2] = data['minute'] + data['second']/60.
    plot_xg = np.zeros(2*n+2, float)
    plot_xg[2:-1:2] = data['cumXg']
    plot_xg[3::2] = data['cumXg']
    
    return pd.DataFrame(data={'time':time, 'xg':plot_xg})

#seperates data by team, plots stepplot and points for goals
def plotXg(data, end, colors=['tab:blue', 'tab:orange'], label_suff=''):
    '''
    data takes dataframe in format given above,
    end takes the end of the game (e.g. 90 miutes) so plot doesnt stop at last shot,
    colors takes optional color arguments,
    label_suff will be appended to the team names in the legend
    '''
    teams = data['team'].unique()
    for team, color in zip(teams,colors):
        data_t = data[data['team']==team].copy()
        data_t['cumXg'] = np.cumsum(data_t['xg'])
        df = cleanLines(data_t, end)
        plt.plot(df['time'], df['xg'], label=team+label_suff, color=color)
        data_g = data_t[data_t['isGoal']]
        plt.scatter(data_g['minute']+data_g['second']/60., data_g['cumXg'], color=color)
    plt.legend()
    plt.xlabel('minute')
    plt.ylabel('cumulative expected goals')

#actual plotting

plt.figure(figsize=(10,7))
plotXg(shots_wy, wyscout.iloc[-1].minute, label_suff=' [Wyscout]')
plt.savefig(save_path+'xg_plot_wyscout.png')

plt.figure(figsize=(10,7))
plotXg(shots_sb, wyscout.iloc[-1].minute, label_suff=' [Statsbomb]')
plt.savefig(save_path+'xg_plot_statsbomb.png')

plt.figure(figsize=(10,7))
plotXg(shots_wy, wyscout.iloc[-1].minute, colors=['tab:blue', 'tab:orange'], label_suff=' [Wyscout]')
plotXg(shots_sb, wyscout.iloc[-1].minute, colors=['lightblue', 'gold'], label_suff=' [Statsbomb]')
plt.savefig(save_path+'xg_plot_compare.png')