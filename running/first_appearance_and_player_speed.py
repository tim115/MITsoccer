import numpy as np

def get_first_appearance(match,id):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get his first appearance.

    Parameters
    ----------
    match: match object parsed

    id: str
        player id in strings
    
    Returns
    ---------
    @return: int
            frame, in which player appears for the first time
    """
    num_frames = len(match.frames)
    for f in range(0,num_frames):
        for p in match.frames[f].trackingObjs:
            if((p.id) == id):
                return f
    return num_frames



def get_player_speed(match, id,first):
    """
    Following @dcamenisch's match parser object, insert a player id
    to get an array of average speeds over one frame.

    Parameters
    ----------
    match: match object parsed

    id: str
        player id in strings
        
    first: int
        frame, in which player appears for the first time
    
    Returns
    ---------
    @return: numpy array
        array of average speeds over one frame
    """
    
    num_frames = len(match.frames)
    v = []
    for f in range(first + 25,num_frames,25):
        for p in match.frames[f-25].trackingObjs:
            if((p.id) == id):
                x1 = int(p.x)/100
                y1 = int(p.y)/100
        for p in match.frames[f].trackingObjs:
            if((p.id) == id):
                x2 = int(p.x)/100
                y2 = int(p.y)/100
                x = x2-x1
                y = y2-y1
                d = np.sqrt(x**2 + y**2)
                v.append(d)
    v = np.array(v)
    k = v > 10
    v = np.delete(v,k)  #delete frame at half-time pause, where players velocity might get too big due to instant displacement            
    return v