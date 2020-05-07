from util.util import *
from util.db_client import DBClient
from util.tweet_sentiment_classifier import TweetSentimentClassifier
from util.tweet_weather_classifer import TweetWeatherClassifier
from dotenv import load_dotenv
import tweepy
import time
from urllib3.exceptions import ReadTimeoutError

load_dotenv()

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
                print(tweet)
                try:
                    db_data = self.prepare_data(status, tweet)
                    self.db_client.tweet_container.create_item(body=db_data)
                    self.count += 1
                except Exception as e:
                    print(f"Something went wrong with tweet. "
                          f"{e}\nContinuing...")

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
    api = init_tweepy()

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
        while True:
            try:
                my_stream.filter(locations=US)
            except ReadTimeoutError:
                continue
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
