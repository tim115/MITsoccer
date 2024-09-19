#modified version of snippet $475
def get_time_played(match, id, startframe):
    """
    inputs:
    match: match object parsed (use @dcamenisch's match parser object)
    id: player id in strings
    startframe: framenumber where the play starts
    
    returns:
    the total time played in minutes by this player in this match.
    """
    num_frames = len(match.frames)
    t = 0
    for f in range(startframe, num_frames):
        for p in match.frames[f].trackingObjs:
            if((p.id) == id):
                t = t+1/25
    
    #convert t from seconds into minutes and round to minutes
    t = t/60
    t = round(t)

    return t