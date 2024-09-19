import numpy as np
import parseData #snippet $396
import get_player_distance_covered as dist #modified snippet $409
import playerInfos #sippet $408
import get_time_played as tp #modified snippet $475
import convert_speed as cs
import matplotlib.pyplot as plt

match = parseData.Match("dataAvN.xml") 
aut = playerInfos.parseSite(8)
mkd = playerInfos.parseSite(59205)

#get the starting time
num_frames = len(match.frames)
startframe = 0
for f in range(0,num_frames):
        if((match.frames[f].ballInPlay) == 1):
                startframe = f
                break

#create & output data
aut_distance_covered = 0
mkd_distance_covered = 0
print("|", "Austria", "|", "Time played in min", "|", "Distance covered in km", "|", "Average Speed", "|", "walking in min", "|", "jogging in min", "|", "running in min", "|", "sprinting in sec", "|", "#sprints", "|")
print("|", "-------", "|", "------------------", "|", "----------------------", "|", "-------------", "|", "--------------", "|", "--------------", "|", "--------------", "|", "----------------", "|", "-----   ", "|")
for p in aut:
        z = tp.get_time_played(match,p.id,startframe)
        if (z>0):
                x = dist.get_player_distance_covered(match,p.id,startframe)
                aut_distance_covered = aut_distance_covered + x
                y = cs.speed_amount(match,p.id,startframe)
                [a,b]=cs.count_sprints_and_times(match,p.id,startframe)
                print("|", p.name, '|', z, "|", x, "|", cs.average_speed(match,p.id,startframe), "|", round(y[0]/60,2), "|", round(y[1]/60,2), "|", round(y[2]/60,2), "|", y[3], "|", a, "|")

print("|", "North Macedonia", "|", "Time played in min", "|", "Distance covered in km", "|", "Average Speed", "|", "walking in min", "|", "jogging in min", "|", "running in min", "|", "sprinting in sec", "|", "#sprints", "|")
print("|", "---------------", "|", "------------------", "|", "----------------------", "|", "-------------", "|", "--------------", "|", "--------------", "|", "--------------", "|", "----------------", "|", "-----   ", "|")
for p in mkd:
        z = tp.get_time_played(match,p.id,startframe)
        if (z>0):
                x = dist.get_player_distance_covered(match,p.id,startframe)
                mkd_distance_covered = mkd_distance_covered + x
                y = cs.speed_amount(match,p.id,startframe)
                [a,b]=cs.count_sprints_and_times(match,p.id,startframe)
                print("|", p.name, '|', z, "|", x, "|", cs.average_speed(match,p.id,startframe), "|", round(y[0]/60,2), "|", round(y[1]/60,2), "|", round(y[2]/60,2), "|", y[3], "|", a, "|")


print("Total distance covered by Austria:", round(aut_distance_covered,1))
print("Total distance covered by North Mazedonia:", round(mkd_distance_covered,1))
print("Difference:", round(aut_distance_covered-mkd_distance_covered,1))
