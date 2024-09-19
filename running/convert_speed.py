from re import S
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import player_speed_vector as psv

def average_speed(match,id,startframe):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get an array of average speeds over one second.

    parameters:
    match: match object parsed
    id: player id in strings
    startframe: framenumber where the play starts

    output: average speed
    """
    v = psv.player_speed(match,id,startframe)
    l = v.size
    av = 0
    if(l>0):
        av = (v.sum())/l
    av = round(av,2)
    return av

def speed_amount(match,id,startframe):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get an array of average speeds over one second.

    parameters:
    match: match object parsed
    id: player id in strings
    startframe: framenumber where the play starts

    output: time spent walking(<=2m/s)/jogging(2m/s-4m/s)/running(4m/s-7m/s)/sprinting(>7m/s) in seconds as an array
    """
    
    v = psv.player_speed(match,id,startframe)
    l = v.size
    walking = 0
    jogging = 0
    running = 0
    sprinting = 0
    for i in range(l):
        if ((v[i]) <= 2):
            walking = walking + 1
        elif ((v[i]) > 7):
            sprinting = sprinting + 1
        elif (2 < (v[i]) <= 4):
            running = running + 1
        else:
            jogging = jogging + 1
    
    return [round(walking/25), round(jogging/25), round(running/25), round(sprinting/25)]

def count_sprints_and_times(match, id, startframe):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get an array of average speeds over one second.

    parameters:
    match: match object parsed
    id: player id in strings
    startframe: framenumber where the play starts

    output: the number of sprints and start-/endframes of each sprint
    """
    v = psv.player_speed_with_time(match,id,startframe)
    l = v.size
    counting = 0
    counter = 0
    x = 0
    numberofsprints = 0
    intervals = []
    for i in range(l):
        if (v[i] > 7):
            if (counting == 0):
                x = i + startframe
            counting = 1
            counter = counter + 1
        else:
            if (counting == 1):
                counting = 0
                if (counter >= 25):
                    numberofsprints = numberofsprints + 1
                    intervals.append([x,i+startframe])
            counter = 0
    return [numberofsprints,intervals]

def plot_sprints(match, id, name, startframe):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get an array of average speeds over one second.

    parameters:
    match: match object parsed
    id: player id in strings
    name: player name
    startframe: framenumber where the play starts

    output: plots the sprints
    """
    [sprints,intervals] = count_sprints_and_times(match,id,startframe)
    fig, ax = plt.subplots()
    ax.set_title(name)
    #create field
    rectangle = pat.Rectangle((-52.5, -34), 105, 68, edgecolor='white', facecolor="green", linewidth=2)
    ax.add_patch(rectangle)
    ax.add_patch(pat.Rectangle((-52.5, -20.16), 16.5, 40.32, edgecolor='white', facecolor="green", linewidth=2))
    ax.add_patch(pat.Rectangle((36, -20.16), 16.5, 40.32, edgecolor='white', facecolor="green", linewidth=2))
    ax.add_patch(pat.Rectangle((-52.5, -9.14), 5.5, 18.28, edgecolor='white', facecolor="green", linewidth=2))
    ax.add_patch(pat.Rectangle((47, -9.14), 5.5, 18.28, edgecolor='white', facecolor="green", linewidth=2))
    ax.add_patch(pat.Circle((0,0),9.15,edgecolor='white', facecolor="green", linewidth=2))
    ax.add_patch(pat.Circle((0,0),1, color='white', linewidth=1))
    ax.add_patch(pat.Circle((-52.5,-3.66),1, color='white', linewidth=1))
    ax.add_patch(pat.Circle((-52.5,3.66),1, color='white', linewidth=1))
    ax.add_patch(pat.Circle((52.5,-3.66),1, color='white', linewidth=1))
    ax.add_patch(pat.Circle((52.5,3.66),1, color='white', linewidth=1))
    ax.add_patch(pat.Circle((-41.5,0),1, color='white', linewidth=1))
    ax.add_patch(pat.Circle((41.5,0),1, color='white', linewidth=1))
    ax.axvline(0,-34,34,color='white',linewidth=2)

    plt.xlim([-52.5, 52.5])
    plt.ylim([-34, 34])
    
    for i in range(sprints):
        start = intervals[i][0]
        #print(start)
        end = intervals[i][1]
        #print(end)
        x_c = []
        y_c = []
        for f in range(start,end):
            for p in match.frames[f].trackingObjs:
                if((p.id) == id):
                    x_c.append(int(p.x)/100)
                    y_c.append(int(p.y)/100)
        ax.plot(x_c,y_c,color='red',linewidth=2)
        ax.arrow(x_c[-2],y_c[-2],(x_c[-1]-x_c[-2]),(y_c[-1]-y_c[-2]),color='red',head_width=3,head_length=3)
    #plt.show()
    return ax

def convert_timestamp_to_framenumber(match, timestamp):
    num_frames = len(match.frames)
    for f in range(num_frames):
        if (match.frames[f].time == timestamp):
            return f

def plot_speed(match, id, name, startframe, startf, endf):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get an array of average speeds over one second.

    parameters:
    match: match object parsed
    id: player id in strings
    name: player name
    startframe: framenumber where the play starts
    startf: framenumber u want the plot to start
    endf: framenumber u want the plot to end

    output: plots the speed of a player starting from frame startf up to frame endf
    """
    v = psv.player_speed_with_time(match,id,startframe)
    l = v.size
    #x0 = np.arange(num_frames)
    k = endf-startf
    x = np.arange(startf-startframe,endf-startframe)
    y = v[startf-startframe:endf-startframe]
    x = x/25/60
    fig, ax = plt.subplots()
    ax.plot(x,y)
    ax.set_ylabel('speed in m/s')
    ax.set_xlabel('time')
    ax.set_title(name)
    plt.show()