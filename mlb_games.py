import mlbgame
import datetime
import statsapi
import requests
import json


def load_teams_json():
    with open("teams_data.json") as teams_file:
        return json.load(teams_file)['teams']


def get_team_id_by_abbv_name(team_abbv_name: str) -> int:
    teams_data = load_teams_json()
    team_abbv_name = "la" if team_abbv_name == "LAD" else team_abbv_name
    team_id = [team['id'] for team in teams_data if team['fileCode'] == team_abbv_name.lower()]
    print(team_abbv_name)
    return team_id[0]


def get_mlb_today_lineup_by_team(team_abbv_name):
    """
    Return dic with players from 2 teams
    """
    today = datetime.datetime.today().date()
    #today ="09/07/2021"
    team_id = get_team_id_by_abbv_name(team_abbv_name=team_abbv_name)
    sched = statsapi.schedule(start_date=today, end_date=today, team=team_id)
    players = []
    for game in sched:
        response = requests.get(
            f'https://statsapi.mlb.com/api/v1/schedule?gamePk={game["game_id"]}&language=en&hydrate=lineups')
        data = response.json()
        if len(data['dates'][0]['games'][0]['lineups']) > 0 :
            home_lineups = data['dates'][0]['games'][0]['lineups']['homePlayers']
            away_lineups = data['dates'][0]['games'][0]['lineups']['awayPlayers']
            for home_player in home_lineups:
                players.append(home_player['fullName'])

            for away_player in away_lineups:
                players.append(away_player['fullName'])

    return players
