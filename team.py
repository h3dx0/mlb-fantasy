import datetime
import json

from oauth import get_oauth_session
from config import YAHOO_ENDPOINT


class Team:
    def __init__(self, team_id):
        self.url = 'team'
        self.team_id = team_id
        self.oauth = get_oauth_session()

    def get_team_info(self):
        response = self.oauth.session.get(
            f'{YAHOO_ENDPOINT}/{self.url}/{self.team_id}/', params={'format': 'json'})
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response.json()

    def get_today_roster(self):
        today = datetime.datetime.today().date()
        response = self.oauth.session.get(
            f'{YAHOO_ENDPOINT}/{self.url}/{self.team_id}/roster;date={today}', params={'format': 'json'})
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response.json()

    def get_roster_as_str_message(self) -> str:
        roster_data = self.get_today_roster()
        roster_players, roster_players_count = self.get_roster_info(roster_data=roster_data)
        players_as_str = self.get_players_info_str(roster_players=roster_players, players_count=roster_players_count)
        return players_as_str

    def get_players_info_str(self, roster_players: dict, players_count: int) -> str:
        players_info_str = ""
        for player_index in range(players_count):
            player_full_data = roster_players[f'{player_index}']['player']
            players_info_str += self.create_single_player_info_str(player_full_data=player_full_data)
        return players_info_str

    def create_single_player_info_str(self, player_full_data: dict) -> str:
        player = self.get_player_info(player_full_info=player_full_data)
        return f'{player["position"]} - {player["name"]} - {player["team"]}\n'

    def get_today_players_info(self):
        roster_data = self.get_today_roster()
        roster_players, roster_players_count = self.get_roster_info(roster_data=roster_data)
        today_players = []
        for player_index in range(roster_players_count):
            player_full_data = roster_players[f'{player_index}']['player']
            today_players.append(self.get_player_info(player_full_info=player_full_data))
        return today_players

    @staticmethod
    def get_player_info(player_full_info: dict) -> dict:
        player_info = player_full_info[0]
        postition_info = player_full_info[1]['selected_position']
        player_name = player_info[2]['name']['full']
        player_team = player_info[6]['editorial_team_abbr'] if 'editorial_team_abbr' in player_info[6] else "IL"
        player_positions = postition_info[1]['position'] if 'position' in postition_info[1] else "IL"
        return {'position': player_positions, 'name': player_name, 'team': player_team}

    @staticmethod
    def get_roster_info(roster_data: dict):
        team_info = roster_data['fantasy_content']['team']
        roster = team_info[1] if type(team_info[0]) is list else team_info[0]
        roster_players = roster['roster']['0']['players']
        players_count = roster_players['count']
        return roster_players, players_count

    def get_mlb_teams_abbv_from_roster(self, roster) -> list:
        teams = [player['team'] for player in roster if player['team'] != 'IL']
        return list(set(teams))

# team = Team(team_id='404.l.79962.t.3')
# print(team.get_roster_as_str_message())
