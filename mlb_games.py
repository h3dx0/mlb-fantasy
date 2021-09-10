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


def get_mlb_today_lineup_by_team_abbv(team_abbv_name):
    """
    Return dic with players from home team and away team
    """
    games = get_today_games_from_team_abbv(team_abbv_name)
    players = []
    # Is a forloop because 1 team can play 2 games in 1 day
    for game in games:
        try:
            home_lineups, away_lineups = get_lineups_from_mlbgame(game)
            players.append(get_players_from_mlb_lineups(away_lineups, home_lineups))
        except LineUpFoundException as error:
            print(error)

    return players


def get_today_games_from_team_abbv(team_abbv_name):
    today = datetime.datetime.today().date()
    # today ="09/07/2021"
    team_id = get_team_id_by_abbv_name(team_abbv_name=team_abbv_name)
    sched = statsapi.schedule(start_date=today, end_date=today, team=team_id)
    return sched


def get_players_from_mlb_lineups(away_lineups, home_lineups):
    players = []
    for home_player in home_lineups:
        players.append(home_player['fullName'])
    for away_player in away_lineups:
        players.append(away_player['fullName'])
    return players


def get_lineups_from_mlbgame(game):
    try:
        response = requests.get(
            f'https://statsapi.mlb.com/api/v1/schedule?gamePk={game["game_id"]}&language=en&hydrate=lineups')
        data = response.json()
        lineups = data['dates'][0]['games'][0]['lineups']
        home_lineups = lineups['homePlayers']
        away_lineups = lineups['awayPlayers']
        return home_lineups, away_lineups
    except Exception:
        raise LineUpFoundException(f"No lineups for {game['game_id']}")


class LineUpFoundException(Exception):
    pass
