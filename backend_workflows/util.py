import tweepy
import json

def read_json(path):
    with open(path, 'r') as f:
        return json.loads(f.read())

def init_tweepy(creds):
    consumer_key = creds.get("consumer_key")
    consumer_secret = creds.get("consumer_secret")
    access_token = creds.get("access_token")
    access_token_secret = creds.get("access_token_secret")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True,
                      wait_on_rate_limit_notify=True)