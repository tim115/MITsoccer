import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate as t
import parseData #snippet $396
import get_player_distance_covered as dist #snippet $409
import playerInfos #snippet $408
import get_time_played as tp #snippet $475
import convert_speed as cs


def get_player_distance_type(match, id):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get the distance covered by type of movement in meters.

    Parameters
    ----------
    match: match object parsed

    id: str
        player id in strings
    
    Returns
    ---------
    @return: list
        total distance covered for the player [walking,jogging,running,sprinting] in meters.
    """
    x_c = []
    y_c = []
    num_frames = len(match.frames)
    walk = 0
    jog = 0
    run = 0
    sprint = 0
    for f in range(num_frames):
        for p in match.frames[f].trackingObjs:
            if((p.id) == id):
                x_c.append(int(p.x)/100)
                y_c.append(int(p.y)/100)
                if(f % 25 == 0):
                    x_c_nump = np.asarray(x_c)
                    y_c_nump = np.asarray(y_c)
                    d = np.sum(np.sqrt(np.add(np.square(x_c_nump[1:] - x_c_nump[0:-1]), np.square(y_c_nump[1:] - y_c_nump[0:-1]))))
                    x_c = []
                    y_c = []
                    if (d <= 2):
                        walk += d
                    if (d > 2 and d <= 4):
                        jog += d
                    if (d > 4 and d <= 7):
                        run += d
                    if(d > 7):
                        sprint += d
    
    return [walk,jog,run,sprint]

match = parseData.Match("dataAvN") 
aut = playerInfos.parseSite(8)
mkd = playerInfos.parseSite(59205)



distance_players = []
plnames = []
for p in aut:
    plnames.append(p.name)
labels = np.asarray(plnames)

for nmbr in aut:
    distance_players.append(get_player_distance_type(match, nmbr))

walking = np.asarray([item[0] for item in distance_players])/1000
jogging = np.asarray([item[1] for item in distance_players])/1000
running = np.asarray([item[2] for item in distance_players])/1000
sprinting = np.asarray([item[3] for item in distance_players])/1000
width = 0.35

fig, ax  = plt.subplots()
ax.bar(labels, walking, width,  label='Walking')
ax.bar(labels, jogging, width,  bottom= walking,label='Jogging')
ax.bar(labels, running, width,  bottom= walking + jogging ,label='Running')
ax.bar(labels, sprinting, width,  bottom= walking + jogging + running,label='Sprinting')
ax.set_ylabel('Distance covered in kilometers')
ax.set_title('Distance covered by type per player for Team')
ax.legend()
plt.gcf().autofmt_xdate()
plt.gcf().subplots_adjust(bottom=0.35)
plt.show()   
