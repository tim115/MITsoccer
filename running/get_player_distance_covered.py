import numpy as np
#modified version of snipped $409

def get_player_distance_covered(match, id, startframe):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get the distance covered in meters.

    Parameters
    ----------
    match: match object parsed

    id: str
        player id in strings

    starframe: int
        framenumber where the play starts
    
    Returns
    ---------
    @return: float
        total distance covered for the player in meters.
    """
    x_c = []
    y_c = []
    num_frames = len(match.frames)
    for f in range(startframe,num_frames):
        for p in match.frames[f].trackingObjs:
            if((p.id) == id):
                x_c.append(int(p.x)/100)
                y_c.append(int(p.y)/100)

    x_c_nump = np.asarray(x_c)
    y_c_nump = np.asarray(y_c)
    m = np.sum(np.sqrt(np.add(np.square(x_c_nump[1:] - x_c_nump[0:-1]), np.square(y_c_nump[1:] - y_c_nump[0:-1]))))
    km = round(m/1000,1)
    return km