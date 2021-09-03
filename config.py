import requests
import json
import webbrowser
import base64

from requests.api import head

SOCIAL_AUTH_YAHOO_OAUTH2_KEY = 'dj0yJmk9YVpHZXdDV2NVNmlsJmQ9WVdrOU5HMVhOMEp0TjNRbWNHbzlNQT09JnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PThk'
SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = '57225bf18895369e5fd08d7737adde63673e0906'
YF_APP_ID = '4mW7Bm7t'
ACCESS_CODE = '53bgcgq'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.yahoo.YahooOpenId',
)
base_url = 'https://api.login.yahoo.com/'

code_url = f'oauth2/request_auth?client_id={SOCIAL_AUTH_YAHOO_OAUTH2_KEY}&redirect_uri=oob&response_type=code&language=en-us'

#webbrowser.open(base_url + code_url)

encoded = base64.b64encode((SOCIAL_AUTH_YAHOO_OAUTH2_KEY +
                           ':' + SOCIAL_AUTH_YAHOO_OAUTH2_SECRET).encode("utf-8"))
headers = {
    'Authorization': f'Basic {encoded.decode("utf-8")}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
"""
get a refresh token
data = {
    'grant_type': 'refresh_token',
    'redirect_uri': 'oob',
    'code': code,
    'refresh_token': refresh_token
}

data = {
    'grant_type': 'authorization_code',
    'redirect_uri': 'oob',
    'code': ACCESS_CODE
}
response = requests.post(base_url + 'oauth2/get_token',
                         headers=headers, data=data)

access_token = response.json()['access_token']
refresh_token = response.json()['refresh_token']
"""
access_token = '51kJVVGfuwbeZ0tNe8TukMHP.GU2cbZbxvXCPnV2VqW8l1cq0Z1du_rOGFb0NqmQA5OL1DuwYH8l2xsMnq0TGGSgGF1GuqKCWPUFggiGRbkHeVUxkE0.ogaBazjPUXegC9wAHrcaVL_JZE4EnUOtBWighTNVGdF4lRNZgihtn14n_eLmIOLp4uUJYZwZpNev3SgndpE4xllDrrbYTzu1o_JkElvovohnyfEGivDOCfhBA3VcyjlAE1eCyTTGeCR_GrSZYmWwllB2n5ySxwylNb__IIW71JJPj1F36eqKExTETuXojD4q3UkrYRAGpUasXr0ym6Tc6Uk7NJ2orVkDZj4mKLFSJ3dkQCjefmsNR.CviLAdm5oNRIPVmkYOGzUHZYR7tE_hroEvGmnrdmzwLAMmtpaVTwehIzmomkNlbs6sQbEF7pxVmlt7962zcrxRYhBLc9sdwFXrQ6bN7owwcWyoMiDVJWInjNKJrr3fTrQ0ahaGQMO8nk3lFdGkIIOG_DL_O.WznsD1ikd4ogAndZ0kEYj0.2CNz_Gl9GfuAN_rNJlGIUGwdQmRTyZkQNl90IRkjhjwbboPRlxDa53facpK8xBEJZjeW59W3piidHYAGh_dmbMcb1jjIY2P.B18AltfMyyWnb0guYClRQuFrb8eDcn6AZTyX1nCZ81A8n_xUJn4fHUXVfyeRfjsMOLT6I8GDLSo1qNYpsGYconGTRo8YbmE.hAEOxLXb4aHSCiIxf0661hJEkK._mDwYbi2.hOQjhWKXHsgsSZBuU8L90.OtFlGZBM3CFN0gkNf08PQcUz3Le4xYqASMoKKEmQ3zr2_MBXZUsPZ_aTsirq2FtjcQTPZi5N8_6y19ndAvHnfVJVbp7VX4NUpKiHRQ5M32E9V8hYZ.51LY.t67hGFGS2bkZRKaMXmaFODAxWRn0zn5gVOnVQ9CHTW8TqfG8qpAKCcbymXIocEIKXABfW.fK61EOxI9TrpotPrKEf5oqdMqQR8o2Bt'
new_headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://fantasysports.yahooapis.com/fantasy/v2/league/', headers=new_headers)

print(response.ok)
