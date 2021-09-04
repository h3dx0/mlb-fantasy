import json

from oauth import get_oauth_session
from config import YAHOO_ENDPOINT
from config import LEAGUE_ID


class League:
    def __init__(self, league_id):
        self.url = 'league'
        self.league_id = league_id
        self.oauth = get_oauth_session()

    def get_general_info(self):
        response = self.oauth.session.get(
            f'{YAHOO_ENDPOINT}/{self.url}/{self.league_id}/', params={'format': 'json'})
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response.json()

    def get_scoreboard(self) -> dict:
        """
        Return the league scoreboard, all matchups information
        :return dict 'matchups' ->dict, 'total_matchups' ->int:
        """
        response = self.oauth.session.get(
            f'{YAHOO_ENDPOINT}/{self.url}/{self.league_id}/scoreboard/', params={'format': 'json'})
        if response.status_code != 200:
            raise RuntimeError(response.content)
        league_data = response.json()
        league_data = league_data['fantasy_content']['league']
        inf = {'scoreboard': data['scoreboard'] for data in league_data if 'scoreboard' in data}
        matchups = inf['scoreboard']['0']['matchups']
        total_matchups = inf['scoreboard']['0']['matchups']['count']
        return {'matchups': matchups, 'total_matchups': total_matchups}

    @staticmethod
    def get_matchups_as_str_message(matchups, total_matchups) ->str:
        """TODO: refactor this method"""
        final_message = ""
        for matchup_index in range(total_matchups):
            teams = matchups[f'{matchup_index}']['matchup']['0']['teams']
            team1 = teams['0']['team']
            team2 = teams['1']['team']
            team_1_data = team1[0] if type(team1[0]) is list else team1[1]
            team_2_data = team2[0] if type(team2[0]) is list else team2[1]
            team_1_stats = team1[0] if type(team1[0]) is dict else team1[1]
            team_2_stats = team2[0] if type(team2[0]) is dict else team2[1]
            team_1_name = team_1_data[2]['name']
            team_2_name = team_2_data[2]['name']

            team_1_points = team_1_stats['team_points']['total']
            team_2_points = team_2_stats['team_points']['total']
            matchup_info = f'{team_1_name}: {team_1_points} VS {team_2_name}: {team_2_points} \n'
            final_message += matchup_info

        return final_message

