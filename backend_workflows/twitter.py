import tweepy
import json
import sys
import time
import csv
from util import *

KEYWORDS = [
    "arid", "autumn", "blizzard", "blustery", "breeze", "chill", "chilly",
    "cloudy", "cold", "colder", "coldest", "downpour", "drizzling", "dry",
    "flurries", "fog", "foggy", "freeze", "freezing", "frost", "gale", "hail", "haze",
    "heat", "hot", "hottest", "humid", "humidity", "mist", "muggy", "overcast",
    "rain", "raining", "rainy", "sizzler", "sleet", "snow", "snowing", "snowy",
    "springtime", "storm", "sun", "sunburn", "sunlight",
    "sunny", "sunscreen", "sunshine", "sweltering", "temperature",
    "thunder", "umbrella", "warm", "warmer", "warmest", "weather", "wind",
    "windy", "°C", "°F"
]

WORDS_TO_IGNORE = [
    "wind:calm","humidity up","humidity down","temperature up",
    "temperature down","dew point","today’s records","trump",
    "#good morning","drinking","gusting","today’s forecast","barometer",
    "weather now","hiring","can you recommend anyone for this job",
    "diabetic", "just posted a photo@", "ice cold","@realDonaldTrump", "POTUS",
    "hot take", "hot dog", "corona", "coronavirus", "cold brew",
    "cold beer",
]

PHX = [-112.524719,33.275435,-111.619720,33.800832]
CA_AZ_NV_UT = [-126.079102,31.090574,-108.720703,42.779275]
WA_OR_ID_MT_VA = [-125.683594,41.902277,-110.566406,49.724479]
AR_FL = [-94.790039,24.966140,-79.672852,36.597889]
MN_IL = [-97.338867,36.562600,-87.495117,49.009051]
KY_ME = [-89.252930,36.527295,-66.445313,47.754098]
US = [-126.210938,24.686952,-66.708984,50.457504]

class Listener(tweepy.StreamListener):
    def __init__(self, output_file=None):
        super(Listener,self).__init__()
        self.output_file = output_file
        self.count = 0

    def on_status(self, status):
        tweet = ""

        # retweet check
        if hasattr(status, "retweeted_status"):
            try:
                tweet = status.retweeted_status.extended_tweet['full_text']
            except AttributeError:  # extended tweet DNE
                tweet = status.retweeted_status.text

        else:
            try:
                tweet = status.extended_tweet['full_text']
            except AttributeError:   # extended tweet DNE
                tweet = status.text

        if has_keyword(tweet):
            tweet = tweet.replace(',', '')
            weather = -1
            sentiment = -1
            link = f"https://twitter.com/{status.user.screen_name}/status/{status.id_str}"
            self.count += 1
            print(self.count)
            print(link)
            print(f"{status.user.screen_name} {status.id_str}: {tweet}")
            print()  # Newline
            if self.output_file:
                with open(self.output_file, 'a+', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow([
                        weather,
                        sentiment,
                        link,
                        status.user.screen_name,
                        status.id_str,
                        tweet
                    ])

    def on_error(self, status_code):
        print(status_code)
        return False

def has_keyword(tweet):
    """
    Given a tweet, does it have one of the keywords?
    True if yes, else False
    """
    temp = tweet.lower()
    for keyword in KEYWORDS:
        if keyword in temp.split():
            for bad_word in WORDS_TO_IGNORE:
                if bad_word in temp:
                    print("IGNORING TWEET", bad_word)
                    print(tweet)
                    print()
                    return False
            return True
    return False




if __name__ == "__main__":
    creds = read_json("./twitter_auth.json")
    api = init_tweepy(creds)

    listener = Listener('output/april10.csv')
    myStream = tweepy.Stream(auth=api.auth, listener=listener)
    try:
        print('Start streaming.')
        all_locations = CA_AZ_NV_UT + WA_OR_ID_MT_VA + AR_FL + MN_IL + KY_ME
        print(all_locations)
        start = time.time()
        myStream.filter(locations=US)
    except KeyboardInterrupt as e :
        print("Stopped.")
    finally:
        total_seconds = time.time() - start
        print(f"{listener.count} tweets in {total_seconds} seconds")
        print(f"{listener.count/total_seconds*60} tweets per minute")
        print('Done.')
        myStream.disconnect()
