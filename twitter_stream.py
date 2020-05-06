from util.util import *
from util.db_client import DBClient
from util.tweet_sentiment_classifier import TweetSentimentClassifier
from util.tweet_weather_classifer import TweetWeatherClassifier
import tweepy
import time


PHX = [-112.524719,33.275435,-111.619720,33.800832]
CA_AZ_NV_UT = [-126.079102,31.090574,-108.720703,42.779275]
WA_OR_ID_MT_VA = [-125.683594,41.902277,-110.566406,49.724479]
AR_FL = [-94.790039,24.966140,-79.672852,36.597889]
MN_IL = [-97.338867,36.562600,-87.495117,49.009051]
KY_ME = [-89.252930,36.527295,-66.445313,47.754098]
US = [-126.210938,24.686952,-66.708984,50.457504]


class Listener(tweepy.StreamListener):
    def __init__(self, db_client, weather_classifier, sentiment_classifier):
        super(Listener, self).__init__()
        self.db_client = db_client
        self.weather_classifier = weather_classifier
        self.sentiment_classifier = sentiment_classifier
        self.count = 0

    def on_status(self, status):

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
            weather = self.weather_classifier.predict(tweet)
            if weather == 1:
                self.count += 1
                db_data = self.prepare_data(status, tweet)
                self.db_client.tweet_container.create_item(body=db_data)

    def on_error(self, status_code):
        print(status_code)
        return False

    def prepare_data(self, status, tweet):
        sentiment = self.sentiment_classifier.predict(tweet)
        lat, long = get_lat_long(status.place.full_name)
        epoch_time = int(status.created_at.timestamp())
        weather_data = get_current_weather_data(lat, long)

        # Add the data to the weather_data json
        weather_data["sentiment"] = sentiment
        weather_data["weather"] = 1
        weather_data["epoch"] = epoch_time
        weather_data["full_name"] = status.place.full_name
        weather_data["id"] = status.id_str

        return weather_data


def main():
    # Init Twitter API
    creds = read_json("./twitter_auth.json")
    api = init_tweepy(creds)

    # Init Classifiers and DB Client
    db_client = DBClient()
    weather_classifier = TweetWeatherClassifier(
        "./data/classified_data.csv")
    sentiment_classifier = TweetSentimentClassifier()
    # sentiment_classifier = None

    # Create tweet listener
    listener = Listener(db_client, weather_classifier,
                        sentiment_classifier)

    my_stream = tweepy.Stream(auth=api.auth, listener=listener)
    start = time.time()
    try:
        my_stream.filter(locations=US)
    except KeyboardInterrupt as e:
        print("Stopped.")
    finally:
        total_seconds = time.time() - start
        print(f"{listener.count} tweets in {total_seconds} seconds")
        print(f"{listener.count/total_seconds*60} tweets per minute")
        print('Done.')
        my_stream.disconnect()


if __name__ == "__main__":
    main()
