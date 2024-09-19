# https://gitlab.ethz.ch/socceranalytics/uefa-euro-2020/-/snippets/555
# 555

import pandas as pd
from socceraction.data.statsbomb import StatsBombLoader
import socceraction.spadl as spadl
import socceraction.vaep.features as fs
import socceraction.vaep.labels as lab
from socceraction.vaep import VAEP
from tqdm import tqdm
import matplotlib.pyplot as plt
import math
import socceraction.xthreat as xthreat

url_grid = "https://karun.in/blog/data/open_xt_12x8_v1.json"
xT_model = xthreat.load_model(url_grid)
pd.set_option("display.max_rows", None)

SBL = StatsBombLoader(getter = "local", root = "../../data/statsbomb360") #TODO: Insert path to StatsBomb Data

#df_games = SBL.games(competition_id=55, season_id=43).set_index("game_id") #TODO: Insert Competition (55) and Season (43) ID

df_events = SBL.events(game_id = 3788747)#TODO-Insert Game ID
df_actions = spadl.statsbomb.convert_to_actions(df_events, home_team_id=915)#TODO: Insert Home-Team ID
df_actions = spadl.play_left_to_right(df_actions, 915) #TODO: Insert Home-Team-ID after ,

df_actions = (
  spadl.add_names(df_actions)
  .merge(SBL.teams(game_id=3788747))#TODO: Insert Game ID
  .merge(SBL.players(game_id=3788747))#TODO: Insert Game ID
)

del df_actions["team_name"]
del df_actions["player_name"]
del df_actions["nickname"]
del df_actions["jersey_number"]
del df_actions["is_starter"]
del df_actions["starting_position_id"]
del df_actions["starting_position_name"]
del df_actions["minutes_played"]

df_actions_ltr = spadl.play_left_to_right(df_actions, 915)#TODO: Insert ID of Home Team
df_actions["xT_value"] = xT_model.rate(df_actions_ltr)

df_players = SBL.players(game_id = 3788747) #TODO: insert Game-ID

max_half_1 = 0
max_half_2 = 0
for k, row in df_actions.iterrows():
    if df_actions['period_id'][k] == 1 and df_actions['time_seconds'][k] > max_half_1:
        max_half_1 = df_actions['time_seconds'][k]
    if df_actions['period_id'][k] == 2 and df_actions['time_seconds'][k] > max_half_2:
        max_half_2 = df_actions['time_seconds'][k]

times = range(int(max_half_1 + max_half_2) + 1)
game_minute = []
for j in range(len(times)):
    game_minute.append(times[j] / 60)

for i, row_players in tqdm(df_players.iterrows()):

    player_VAEP = [0]
    player_id = df_players['player_id'][i]

    for k in tqdm(range(1, int(len(times)))):
        toadd = player_VAEP[-1]
        for j in range(len(df_actions.index)):
            if df_actions['period_id'][j] == 2:
                time_of_action = max_half_1 + df_actions['time_seconds'][j]
            else:
                time_of_action = df_actions['time_seconds'][j]
            if df_actions['player_id'][j] == player_id:
                if int(time_of_action) == times[k] and not math.isnan(df_actions['xT_value'][j]):
                    toadd += df_actions['xT_value'][j]
        player_VAEP.append(toadd)
    fig, ax = plt.subplots()
    plt.plot(game_minute, player_VAEP)
    fig.suptitle(str(df_players['player_name'][i]))
    ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])
    ax.set_xlabel("Game Minute")
    ax.set_ylabel("xT Player Rating")
    plt.savefig(str(df_players['player_name'][i]) + " xT Player Rating")
    plt.clf()
