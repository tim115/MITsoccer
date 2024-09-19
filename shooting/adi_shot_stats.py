from typing import List
from kloppy import statsbomb
#import bz2
from mplsoccer.pitch import Pitch
import time

dataset = statsbomb.load(
    #event_data=bz2.open("./data/statsbomb360/3788741/events.json.bz2"),
    event_data="/Users/adrianmuller/Desktop/soccer-analytics-repo/data/statsbomb360/events/3788747.json",
    lineup_data="/Users/adrianmuller/Desktop/soccer-analytics-repo/data/statsbomb360/lineups/3788747.json",
    coordinates="statsbomb",
    event_types=["shot"],
)

x_list: List[float] = []
y_list: List[float] = []
dx_list: List[float] = []
dy_list: List[float] = []
color_list: List[float] = []

pitch = Pitch(
    pitch_color="g", line_zorder=1, line_color="white", pitch_type="statsbomb", 
    figsize=(2048,1408), constrained_layout=False, tight_layout=False #resize bigger
)
fig, ax = pitch.draw()

fig.set_size_inches(9.25,5.25) #resize bigger
for event in dataset.events:
    raw_event = event.raw_event
    [x_start, y_start] = raw_event["location"]
    x_end = raw_event["shot"]["end_location"][0]
    y_end = raw_event["shot"]["end_location"][1]
    
    #Invert coordinates if goal from Sweden 
    if raw_event["team"]["name"] == "Ukraine":
        x_start = 120-x_start
        x_end = 120-x_end
        y_start = 80-y_start
        y_end = 80-y_end
    
    x_list.append(x_start)
    y_list.append(y_start)
    dx_list.append(x_end - x_start)
    dy_list.append(y_end - y_start)
    
    is_goal = raw_event["shot"]["outcome"]["name"] == "Goal"
    #color_list.append(1 if is_goal else 0)
    
    is_blocked = raw_event["shot"]["outcome"]["name"] == "Blocked"
      
    #sometimes the deflected key does not exist, therefore use getter function
    is_deflected = raw_event.get("shot").get("deflected") == True #raw_event["shot"]["deflected"] 

    #create color map
    if is_goal:
        color_list.append(1)
    elif is_blocked:
        color_list.append(2)
    elif is_deflected:
        color_list.append(3)
    else:
        color_list.append(0)
    
#print(color_list)
arrows = ax.quiver(
    x_list,
    y_list,
    dx_list,
    dy_list,
    color_list,
    angles="xy",
    scale_units="xy",
    scale=1.5,
    #label={"goals", "blocked", "deflected"}
)

#add legend that shows what color means what happened to the shot

#adds text boxes left and right of pitch to show teams
props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)

ax.text(-0.11, 0.53, "SWE", transform=ax.transAxes, fontsize=14,
        verticalalignment="top", bbox=props)
ax.text(1.02, 0.53, "UKR", transform=ax.transAxes, fontsize=14,
        verticalalignment="top", bbox=props)


fig.savefig("shotsOnGoal_multiproperties.png")