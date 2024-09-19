### https://gitlab.ethz.ch/socceranalytics/uefa-euro-2020/-/snippets/533
# 533

import pandas as pd
from socceraction.data.statsbomb import StatsBombLoader
import socceraction.spadl as spadl
import socceraction.vaep.features as fs
import socceraction.vaep.labels as lab
from socceraction.vaep import VAEP
from tqdm import tqdm
import matplotlib.pyplot as plt


VAEP_model = VAEP(nb_prev_actions = 3) #TO-DO fill out, recommended (and default) by original authors is 3
#Load all games with which the model will be trained
SBL = StatsBombLoader(getter = "local", root = '../../data/statsbomb360')#fill in root directory for StatsBomb Data)
df_games = SBL.games(competition_id=55, season_id=43).set_index("game_id") #fill out - if model is trained with EURO 2020 data, competition_id = 55 and season_id = 43
all_features, all_labels = [], []
for game_id, game in tqdm(list(df_games.iterrows())):
    # load the game's events
    game_events = SBL.events(game_id)
    # convert the events to actions
    game_home_team_id = df_games.at[game_id, "home_team_id"]
    game_actions = spadl.statsbomb.convert_to_actions(game_events, game_home_team_id)
    # compute features and labels
    all_features.append(VAEP_model.compute_features(game, game_actions))
    all_labels.append(VAEP_model.compute_labels(game, game_actions))
# combine all features and labels in a single dataframe
all_features = pd.concat(all_features)
all_labels = pd.concat(all_labels)
#Fit your model
VAEP_model.fit(all_features, all_labels)
#load events and actions of game you want to analyze
df_events = SBL.events(game_id = 3788747) #TO-DO add game ID
df_actions = spadl.statsbomb.convert_to_actions(df_events, home_team_id=915) #TO-DO add Home-Team ID

df_actions = (
  spadl.add_names(df_actions)
  .merge(SBL.teams(game_id=3788747)) #TO-DO add game ID
  .merge(SBL.players(game_id=3788747)) #TO-DO add game ID
)
#delete categories so it fits into the ratings function
del df_actions["team_name"]
del df_actions["player_name"]
del df_actions["nickname"]
del df_actions["jersey_number"]
del df_actions["is_starter"]
del df_actions["starting_position_id"]
del df_actions["starting_position_name"]
del df_actions["minutes_played"]
#rate each action of the game
ratings = VAEP_model.rate(df_games.loc[3788747], df_actions) #TO-DO add game ID in []
#get all players of the game
df_players = SBL.players(game_id = 3788747) #TO-DO add game-ID
#calculate seconds played for each half
max_half_1 = 0
max_half_2 = 0
for k, row in df_actions.iterrows():
    if df_actions['period_id'][k] == 1 and df_actions['time_seconds'][k] > max_half_1:
        max_half_1 = df_actions['time_seconds'][k]
    if df_actions['period_id'][k] == 2 and df_actions['time_seconds'][k] > max_half_2:
        max_half_2 = df_actions['time_seconds'][k]
#get time-axis
times = range(int(max_half_1 + max_half_2) + 1)
game_minute = []
for j in range(len(times)):
    game_minute.append(times[j] / 60)

df_actions = df_actions.join(ratings)
#evaluate the actions for each player and create an array with the netto VAEP for every second
for i, row_players in tqdm(df_players.iterrows()):
    player_VAEP = [0]
    player_id = df_players['player_id'][i]
    #loop through every second
    for k in tqdm(range(1, int(len(times)))):
        toadd = player_VAEP[-1] #if no action takes place at this second, player rating stays constant
        for j in range(len(df_actions.index)): #loop through all actions
            if df_actions['period_id'][j] == 2:
              time_of_action = max_half_1 + df_actions['time_seconds'][j]
            else:
              time_of_action = df_actions['time_seconds'][j]
           if df_actions['player_id'][j] == player_id:
              if int(time_of_action) == times[k]:
                 toadd += df_actions['vaep_value'][j] #if considered player has an action at this point in time, take it into account
        player_VAEP.append(toadd)
    #plot the figure
    fig, ax = plt.subplots()
    plt.plot(game_minute, player_VAEP)
    fig.suptitle(str(df_players['player_name'][i]))
    ax.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90])
    ax.set_xlabel("Game Minute")
    ax.set_ylabel("VAEP Player Rating")
    plt.savefig(str(df_players['player_name'][i]) + " VAEP Player Rating")
    plt.clf()

