import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.projections import get_projection_class
from matplotlib.patches import Arc


### SNIPPET 485
#https://gitlab.ethz.ch/socceranalytics/uefa-euro-2020/-/snippets/485

def json_to_normalized_dataframe(path):
    rd = ""
    with open(path, 'r', encoding="UTF-8") as f:
        rd = f.read()
    obj = json.loads(rd)
    df = pd.json_normalize(obj)
    return df

def draw_pitch():
    fig, ax = plt.subplots(figsize = (10.5, 6.8), dpi=300)

    ax.plot([0,0],[0,80], color="black")
    ax.plot([0,120],[80,80], color="black")
    ax.plot([120,120],[80,0], color="black")
    ax.plot([120,0],[0,0], color="black")
    ax.plot([60,60],[0,80], color="black")


    #Left Penalty Area
    ax.plot([18,18],[62,18],color="black")
    ax.plot([0,18],[62,62],color="black")
    ax.plot([18,0],[18,18],color="black")


    #Right Penalty Area
    ax.plot([120,102],[18,18],color="black")
    ax.plot([102,102],[18,62],color="black")
    ax.plot([102,120],[62,62],color="black")
     #Left 6-yard Box
    ax.plot([0,6],[30,30],color="black")
    ax.plot([6,6],[30,50],color="black")
    ax.plot([0,6],[50,50],color="black")
      #Right 6-yard Box
    ax.plot([114,120],[30,30],color="black")
    ax.plot([114,114],[30,50],color="black")
    ax.plot([114,120],[50,50],color="black")


    #Prepare Circles
    centreCircle = plt.Circle((60,40),8.7,color="black",fill=False)
    centreSpot = plt.Circle((60,40),0.8,color="black")
    leftPenSpot = plt.Circle((12,40),0.8,color="black")
    rightPenSpot = plt.Circle((108,40),0.8,color="black")


    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    #Prepare Arcs
    leftArc = Arc((12,40),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((108,40),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="black")

    #Goals
    ax.plot([-3,0],[44,44],color="black")
    ax.plot([-3,-3],[44,36],color="black")
    ax.plot([-3,0],[36,36],color="black")

    ax.plot([123,120],[44,44],color="black")
    ax.plot([123,123],[44,36],color="black")
    ax.plot([123,120],[36,36],color="black")

    #Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)
    
    ax.set_xticks([])
    ax.set_yticks([])

    return ax

def reverse_direction_of_play(x, y, dim_h=120., dim_v=80., origin=(0.,34.)):
    """
    Parameters
    ----------
    x: an array containing the horizontal positions of the player
    y: an array containing the vertical positions of the player
    dim_h (default 105): length of the pitch
    dim_v (default 68): width of the pitch
    origin (default(0,34)): location of the origin in the reference system

    Returns
    --------
    @return: arrays with the positions of the players mirrored with respect to the origin
    """
    x = dim_h/2 - x + origin[0]
    y = dim_v/2 - y + origin[1]
    return x, y


def get_free_kick_coordinates(df, team_name):
    #select event type: short passes, crosses and shots from free_kicks
    df_passes_first = df[(df["pass.type.id"] == 62) & (df["team.name"] == team_name) & (df["period"]==1)]
    df_crosses_first = df[(df["pass.type.id"] == 62) & (df["team.name"] == team_name) & (df["pass.cross"] == 1) & (df["period"]==1)]
    df_shots_first = df[(df["shot.type.id"] == 62) & (df["team.name"] == team_name)& (df["period"]==1)]
    df_passes_second = df[(df["pass.type.id"] == 62) & (df["team.name"] == team_name) & (df["period"]==2)]
    df_crosses_second = df[(df["pass.type.id"] == 62) & (df["team.name"] == team_name) & (df["pass.cross"] == 1)& (df["period"]==2)]
    df_shots_second = df[(df["shot.type.id"] == 62) & (df["team.name"] == team_name)& (df["period"]==2)]

    passes_x = np.array(range(len(df_passes_first)+len(df_passes_second)), dtype="float_")
    passes_y = np.array(range(len(df_passes_first)+len(df_passes_second)), dtype="float_")
    passes_x_to = np.zeros_like(passes_x)
    passes_y_to = np.zeros_like(passes_y)
    crosses_x = np.array(range(len(df_crosses_first)+len(df_crosses_second)), dtype="float_")
    crosses_y = np.array(range(len(df_crosses_first)+len(df_crosses_second)), dtype="float_")
    crosses_x_to = np.zeros_like(crosses_x)
    crosses_y_to = np.zeros_like(crosses_y)
    shots_x = np.array(range(len(df_shots_first)+len(df_shots_second)), dtype="float_")
    shots_y = np.array(range(len(df_shots_first)+len(df_shots_second)), dtype="float_")
    shots_x_to = np.zeros_like(shots_x)
    shots_y_to = np.zeros_like(shots_y)
    
    for i, location in enumerate(df_passes_first["location"]):
        #make sure the home team is always attacking from right to left
        passes_x[i] = location[0]
        passes_y[i] = location[1]

    for i, location in enumerate(df_passes_first["pass.end_location"]):
        passes_x_to[i] = location[0]
        passes_y_to[i] = location[1]


    for i, location in enumerate(df_passes_second["location"]):
        #if the free kick was taken during the second half, reverse the direction of play
        reverse_direction_of_play(location[0], location[1], origin=(60.,40.))
        passes_x[i+len(df_passes_first)] = location[0]
        passes_y[i+len(df_passes_first)] = location[1]

    for i, location in enumerate(df_passes_second["pass.end_location"]):
        reverse_direction_of_play(location[0], location[1], origin=(60.,40.))
        passes_x_to[i+len(df_passes_first)] = location[0]
        passes_y_to[i+len(df_passes_first)] = location[1] 
    
    for i, location in enumerate(df_crosses_first["location"]):
        #make sure the home team is always attacking from right to left
        crosses_x[i] = location[0]
        crosses_y[i] = location[1]

    for i, location in enumerate(df_crosses_first["pass.end_location"]):
        crosses_x_to[i] = location[0]
        crosses_y_to[i] = location[1]

    for i, location in enumerate(df_crosses_second["location"]):
        #if the free kick was taken during the second half, reverse the direction of play
        reverse_direction_of_play(location[0], location[1], origin=(60.,40.))
        crosses_x[i+len(df_crosses_first)] = location[0]
        crosses_y[i+len(df_crosses_first)] = location[1]

    for i, location in enumerate(df_crosses_second["pass.end_location"]):
        reverse_direction_of_play(location[0], location[1], origin=(60.,40.))
        crosses_x_to[i+len(df_crosses_first)] = location[0]
        crosses_y_to[i+len(df_crosses_first)] = location[1] 

    for i, location in enumerate(df_shots_first["location"]):
        #make sure the home team is always attacking from right to left
        shots_x[i] = location[0]
        shots_y[i] = location[1]

    for i, location in enumerate(df_shots_first["shot.end_location"]):
        shots_x_to[i] = location[0]
        shots_y_to[i] = location[1]

    for i, location in enumerate(df_shots_second["location"]):
        #if the free kick was taken during the second half, reverse the direction of play
        reverse_direction_of_play(location[0], location[1], origin=(60.,40.))
        shots_x[i+len(df_shots_first)] = location[0]
        shots_y[i+len(df_shots_first)] = location[1]

    for i, location in enumerate(df_shots_second["shot.end_location"]):
        reverse_direction_of_play(location[0], location[1], origin=(60.,40.))
        shots_x_to[i+len(df_shots_first)] = location[0]
        shots_y_to[i+len(df_shots_first)] = location[1] 

    return np.transpose(np.array([passes_x, passes_y])), np.transpose(np.array([passes_x_to, passes_y_to])), np.transpose(np.array([crosses_x, crosses_y])), np.transpose(np.array([crosses_x_to, crosses_y_to])), np.transpose(np.array([shots_x, shots_y])), np.transpose(np.array([shots_x_to, shots_y_to]))
    
def plot_free_kicks(df, pitch, team_name = "",  pass_color="blue", shot_color="red", cross_color="orange"):
    """
    Plots free kicks divided by play-type: passes, crosses and shots

    Parameters
    ----------
    df: dataframe of the match events
    pitch: axes where the events will be drawn
    team_name: str, name of the team
    pass_color...: color in which a specific type of event has to be plotted
    """
    passes, passes_to, crosses, crosses_to, shots, shots_to = get_free_kick_coordinates(df, team_name)
    for i in range(len(passes)):
        pitch.plot(passes[i,0], passes[i,1], marker='o', color=pass_color, linestyle='')
        pitch.arrow(passes[i,0], passes[i,1], passes_to[i,0]-passes[i,0], passes_to[i,1]-passes[i,1], head_width=1, color=pass_color)
    for i in range(len(crosses)):
        pitch.plot(crosses[i,0], crosses[i,1], marker='o', color=cross_color, linestyle='')
        pitch.arrow(crosses[i,0], crosses[i,1], crosses_to[i,0]-crosses[i,0], crosses_to[i,1]-crosses[i,1], head_width=1, color=cross_color)
    for i in range(len(shots)):
        pitch.plot(shots[i,0], shots[i,1], marker='o', color=shot_color, linestyle='')
        pitch.arrow(shots[i,0], shots[i,1], shots_to[i,0]-shots[i,0], shots_to[i,1]-shots[i,1], head_width=1, color=shot_color)
    plt.title("Free kicks execution for " + team_name)
    
    plt.savefig(team_name+"_free_kicks.png")

pitch = draw_pitch()

df_events = json_to_normalized_dataframe("../../data/statsbomb360/events/3788747.json")

plot_free_kicks(df_events, pitch, team_name="North Macedonia")

