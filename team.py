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

    def get_roster_as_str_message(self):
        roster_data = self.get_today_roster()
        roster_players, players_count = self.get_roster_info(roster_data=roster_data)
        players_str = self.get_players_info_str(roster_players=roster_players, players_count=players_count)
        return players_str

    @staticmethod
    def get_player_info(player_full_info):
        player_info = player_full_info[0]
        postition_info = player_full_info[1]['selected_position']
        player_name = player_info[2]['name']['full']
        player_team = player_info[6]['editorial_team_abbr'] if 'editorial_team_abbr' in player_info[6] else "IL"
        player_positions = postition_info[1]['position'] if 'position' in postition_info[1] else "IL"
        return player_positions, player_name, player_team

    def get_players_info_str(self, roster_players, players_count):
        players_info_str = ""
        for player_index in range(players_count):
            player_full_data = roster_players[f'{player_index}']['player']
            players_info_str += self.get_single_player_info(player_full_data=player_full_data)
        return players_info_str

    def get_single_player_info(self, player_full_data):
        player_positions, player_name, player_team = self.get_player_info(player_full_info=player_full_data)
        return f'{player_positions} - {player_name} - {player_team}\n'

    @staticmethod
    def get_roster_info(roster_data):
        team_info = roster_data['fantasy_content']['team']
        roster = team_info[1] if type(team_info[0]) is list else team_info[0]
        roster_players = roster['roster']['0']['players']
        players_count = roster_players['count']
        return roster_players, players_count
#team = Team(team_id='404.l.79962.t.3')
#print(team.get_roster_as_str_message())