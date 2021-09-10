from team import Team
from mlb_games import get_mlb_today_lineup_by_team


def get_today_fantasy_roster_status():
    fantasy_team = Team(team_id='404.l.79962.t.3')
    fantasy_roster = fantasy_team.get_today_players_info()
    mlb_teams_abbv = fantasy_team.get_mlb_teams_abbv_from_roster(roster=fantasy_roster)
    mlb_rosters = get_mlb_rosters_from_fantasy_roster(fantasy_teams=mlb_teams_abbv)

    return fantasy_players_status(fantasy_roster, mlb_rosters)


def fantasy_players_status(fantasy_roster, mlb_rosters):
    players_lineup = []
    for player in fantasy_roster:
        player['in_lineup'] = True
        for mlb_roster in mlb_rosters:
            if player['team'] == mlb_roster['team']:
                if player['name'] not in mlb_roster['lineup']:
                    player['in_lineup'] = False
                players_lineup.append(player)
    return players_lineup


def get_mlb_rosters_from_fantasy_roster(fantasy_teams):
    mlb_rosters = []
    for team in fantasy_teams:
        today_lineup = get_mlb_today_lineup_by_team(team_abbv_name=team)
        if len(today_lineup):
            mlb_rosters.append({'team': team, 'lineup': today_lineup})
    return mlb_rosters
