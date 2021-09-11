from fantasy_team import FantasyTeam
from mlb_games import get_mlb_today_lineup_by_team_abbv, get_mlb_rosters_by_teams_abbv


def get_today_fantasy_roster_status():
    fantasy_team = FantasyTeam(team_id='404.l.79962.t.3')
    fantasy_roster = fantasy_team.get_today_players_info()
    mlb_teams_abbv = fantasy_team.get_mlb_teams_abbv_from_roster(roster=fantasy_roster)
    mlb_rosters = get_mlb_rosters_by_teams_abbv(mlb_teams_abbv=mlb_teams_abbv)

    return fantasy_team.fantasy_players_status(fantasy_roster, mlb_rosters)

