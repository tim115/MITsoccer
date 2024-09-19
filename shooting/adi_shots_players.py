import pandas as pd
import json

filename = "/Users/adrianmuller/Desktop/soccer-analytics-repo/data/statsbomb360/events/3788747.json" # TODO: insert the filename of your StatBomb's data 
	
with open(filename, encoding='utf8') as f:
    statsb = pd.json_normalize(json.load(f))

def shooter_total(player):
    local_df = statsb.copy(deep=True)
    local_df = local_df[local_df["type.name"]=="Shot"]
    local_df = local_df[local_df["player.name"]==player]
    tot_shot = local_df.shape[0]
    if tot_shot>0:
        goal_mask = (local_df["shot.outcome.name"]=="Goal")
        saved_mask = (local_df["shot.outcome.name"]=="Saved") | (local_df["shot.outcome.name"]=="Saved To Post")
        on_goal = local_df[((goal_mask) | (saved_mask))].shape[0]
        goal = local_df[(goal_mask)].shape[0]
        accuracy = round(on_goal/tot_shot*100,2)
        xg = round(local_df["shot.statsbomb_xg"].sum(),2)
    else:
        return []
    return [tot_shot,on_goal,goal,f"{accuracy}%",xg]

def all_players(df, home_team=True):
    team_dict = {}
    if home_team == True:
        for i in df["tactics.lineup"][0]:
            team_dict[i['player']['name']] = []
        for i, r in df[((df["type.name"]=="Substitution") & (df["team.name"]==df["team.name"][0]))].iterrows():
            team_dict[r["substitution.replacement.name"]] = []

    else:
        for i in df["tactics.lineup"][1]:
            team_dict[i['player']['name']] = []
        for i, r in df[((df["type.name"]=="Substitution") & (df["team.name"]==df["team.name"][1]))].iterrows():
            team_dict[r["substitution.replacement.name"]] = []

    return team_dict

for team in [True, False]:
    team_dict = all_players(statsb,home_team=team)
    tot_team=0
    completed_team=0
    goals_team=0
    xg_team=0
    print("|Player|Total shots|Shots on goal|Goals|Accuracy|Expected goals|")
    print("|---|---|---|---|---|---|")
    for player_name, loc in team_dict.items():
        p = shooter_total(player_name)
        if p!=[]:
            print("|{}|{}|".format(player_name,"|".join(str(pp) for pp in p)))
            tot_team+=p[0]
            completed_team+=p[1]
            goals_team+=p[2]
            xg_team+=p[4]
    print(f"|**Team**|{tot_team}|{completed_team}|{goals_team}|{round(completed_team/tot_team*100,2)}%|{round(xg_team,2)}|\n")