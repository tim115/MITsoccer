def get_player_name(id, team_1, team_2):
    """
    Following @dcamenisch's parseSite code, returns the player name
    given the team numbers from the site. In the example team_1 is 
    Italy and team_2 is Spain. You can check for your own team's id.
    
    """
    home_list = team_1
    for p in home_list:
        if p.id == id:
            return p.name
    away_list = team_2
    for p in  away_list:
        if p.id == id:
            return p.name