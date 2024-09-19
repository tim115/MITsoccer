import numpy as np
#modified version of snipped $423

def player_speed(match, id, startframe):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get an array of average speeds over one second.

    parameters:
    match: match object parsed
    id: player id in strings
    startframe: framenumber where the play starts

    output: array of speeds in m/s over one second for every frame the player was on the field
    """
    
    x_c = []
    y_c = []
    num_frames = len(match.frames)
    for f in range(startframe, num_frames):
        for p in match.frames[f].trackingObjs:
            if((p.id) == id):
                x_c.append(int(p.x)/100)
                y_c.append(int(p.y)/100)

    x_c_nump = np.asarray(x_c)
    y_c_nump = np.asarray(y_c)
    v =  np.asarray(25*np.sqrt(np.add(np.square(x_c_nump[1:] - x_c_nump[0:-1]), np.square(y_c_nump[1:] - y_c_nump[0:-1]))))
    #remove to big speeds that might appear at half time
    k = v > 13
    v=np.delete(v,k)
    return v



def player_speed_with_time(match, id, startframe):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get an array of average speeds over one second.

    parameters:
    match: match object parsed
    id: player id in strings
    startframe: framenumber where the play starts

    output: array of speeds in m/s over one second for every frame of the game
    """
    
    x_c = []
    y_c = []
    num_frames = len(match.frames)
    firstappearance = startframe
    lastappearance = num_frames
    for f in range(startframe, num_frames):
        b=0
        for p in match.frames[f].trackingObjs:
            if((p.id) == id):
                x_c.append(int(p.x)/100)
                y_c.append(int(p.y)/100)
                b=1
        if (b == 0):
            if (x_c == []):
                firstappearance = f+1
            elif (f <= lastappearance):
                lastappearance = f


    x_c_nump = np.asarray(x_c)
    y_c_nump = np.asarray(y_c)
    v0 =  np.asarray(25*np.sqrt(np.add(np.square(x_c_nump[1:] - x_c_nump[0:-1]), np.square(y_c_nump[1:] - y_c_nump[0:-1]))))
    #replace to big speeds that might appear at half time by 0
    for j in range(v0.size):
        if (v0[j] > 13):
            v0[j] = 0
    fa = np.zeros(firstappearance-startframe)
    fl = np.zeros(num_frames-lastappearance)
    v = np.append(fa,v0)
    v = np.append(v,fl)
    v = np.asarray(v)
    return v