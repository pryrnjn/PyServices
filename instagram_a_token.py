from instagram.client import InstagramAPI
import sys

import requests
import json

if len(sys.argv) > 1 and sys.argv[1] == 'local':
    # try:
    #     from test_settings import *
    #
    #     InstagramAPI.host = test_host
    #     InstagramAPI.base_path = test_base_path
    #     InstagramAPI.access_token_field = "access_token"
    #     InstagramAPI.authorize_url = test_authorize_url
    #     InstagramAPI.access_token_url = test_access_token_url
    #     InstagramAPI.protocol = test_protocol
    # except Exception:
    #     pass
    pass
# Fix Python 2.x.
try:
    import __builtin__

    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass

client_id = "7334de047881464abb78fa2ee438d154"  # input("Client ID: ").strip()
client_secret = "8438f728ca2944d086c119aca1fbce34"  # input("Client Secret: ").strip()
redirect_uri = "http://pryrnjn.in"  # input("Redirect URI: ").strip()
# raw_scope = input("Requested scope (separated by spaces, blank for just basic read): ").strip()
scope = ["public_content"]  # raw_scope.split(' ')
# For basic, API seems to need to be set explicitly
if not scope or scope == [""]:
    scope = ["public_content"]

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
login_redirect_uri = api.get_authorize_login_url(scope=scope)

print ("Visit this page and authorize access in your browser: " + login_redirect_uri)

code = (str(input("Paste in code in query string after redirect: ").strip()))

# access_token = api.exchange_code_for_access_token(code)
url = u'https://api.instagram.com/oauth/access_token'
data = {
    u'client_id': client_id,
    u'client_secret': client_secret,
    u'code': code,
    u'grant_type': u'authorization_code',
    u'redirect_uri': redirect_uri
}

response = requests.post(url, data=data)

account_data = json.loads(response.content)
print ("access token: ")
print (account_data)

