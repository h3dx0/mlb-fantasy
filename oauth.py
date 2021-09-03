from yahoo_oauth import OAuth2

oauth = OAuth2(None, None, from_file='secrets.json')
if not oauth.token_is_valid():
    oauth.refresh_access_token()
