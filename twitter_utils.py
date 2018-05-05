import oauth2
import urllib.parse as urlparse

CONSUMER_KEY = "b1t6kQj21Qy3N21IRZHrpYlTd"
CONSUMER_SECRET = "csuOoeCXrhkvyfCVE6V1bzQ4zQMvAe0MC2Zfkv8j8uGo1MjgfY"

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"
AUTH_URL = "https://api.twitter.com/oauth/authorize"

consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
client = oauth2.Client(consumer)


def request_token():
    response, content = client.request(REQUEST_TOKEN_URL, "POST")
    if response.status != 200:
        print("request token error!")
    return dict(urlparse.parse_qsl(content.decode("UTF-8")))

def request_token_url(request_token):
    return "{}?oauth_token={}".format(AUTH_URL, request_token["oauth_token"])

def access_token(request_token, auth_verifier):
    token = oauth2.Token(request_token["oauth_token"], request_token["oauth_token_secret"])
    token.set_verifier(auth_verifier)

    client = oauth2.Client(consumer, token)

    response, content = client.request(ACCESS_TOKEN_URL, "POST")
    if response.status != 200:
        print("error!!!")

    return dict(urlparse.parse_qsl(content.decode("UTF-8")))




