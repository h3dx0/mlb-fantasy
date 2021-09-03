from yahoo_oauth import OAuth2

YAHOO_ENDPOINT = 'https://fantasysports.yahooapis.com/fantasy/v2'
# https://fantasysports.yahooapis.com/fantasy/v2/game/mlb


class Team():
    def __init__(self, oauth, team_id):
        self.url = 'team'
        self.team_id = team_id
        self.oauth = oauth

    def get_team_info(self):
        response = self.oauth.session.get(
            f'{YAHOO_ENDPOINT}/{self.url}/{self.team_id}/', params={'format': 'json'})
        if response.status_code != 200:
            raise RuntimeError(response.content)
        return response.json()


oauth = OAuth2(None, None, from_file='secrets.json')
team = Team(oauth=oauth, team_id='404.l.79962.t.3')

print(team.get_team_info())
