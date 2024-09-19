import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tabulate import tabulate as t
import parseData  # snippet $396
import get_player_distance_covered as dist  # snippet $409
import playerInfos  # snippet $408
import get_time_played as tp  # snippet $475
import convert_speed as cs
import first_appearance_and_player_speed as faps  # snippet $423
import player_speed_vector as psv


match = parseData.Match("dataAvN")
#aut = playerInfos.parseSite(8)

num_frames = len(match.frames)
startframe = 0
for f in range(0, num_frames):
    if((match.frames[f].ballInPlay) == 1):
        startframe = f
        break

v = cs.plot_speed(match, "250043103", "Mr. X", startframe, 70000, 80000)

# for p in aut:
#    cs.plot_speed(match,p.id,p.name)
