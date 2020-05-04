from util import *
import csv
import os
import tqdm
import tweepy
import time


def read_tweet_csv(path):
    field_names = [
        'weather',
        'sentiment',
        'url',
        'user_name',
        'tweet_id',
        'tweet'
    ]
    tweets = []
    with open(path, 'r',  encoding='utf-8') as f:
        reader = csv.DictReader(f, fieldnames=field_names)
        for row in reader:
            tweets.append(row)
    return tweets


def write_full_tweet_csv(path, tweets):
    field_names = [
        'weather',
        'sentiment',
        'url',
        'user_name',
        'tweet_id',
        'date',
        'tweet'
    ]
    file_exists = os.path.isfile(path)
    with open(path, 'a+',  encoding='utf-8',  newline='') as f:
        writer = csv.DictWriter(f, delimiter=',', fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
        for tweet in tweets:
            writer.writerow(tweet)


def get_tweet_date(api, tweet_id):
    """
    i was silly and did not collect the tweets' date field in my initial code.
    That will be fixed, but this is the backfill for that information
    This script simply returns the date string for a tweet.
    That and all other tweet information will be saved back to a csv file.
    """
    date = None
    try:
        full_tweet = api.get_status(tweet_id, tweet_mode='extended')
        date = str(full_tweet.created_at)
    # I think this is built into tweepy but this is a justincase
    except tweepy.RateLimitError:
        print(f"Rate limit reached. sleeping for 15 minute timeout")
        time.sleep(15*60)
        full_tweet = api.get_status(tweet_id, tweet_mode='extended')
    except tweepy.TweepError:
        # print("problem getting tweet. Likely deleted. continuing...")
        pass

    return date


if __name__ == "__main__":
    credentials = read_json("./twitter_auth.json")
    api = init_tweepy(credentials)
    tweets = read_tweet_csv('output/april10.csv')
    full_tweets = []
    for tweet in tqdm.tqdm(tweets, desc="getting tweet dates"):
        tweet_date = get_tweet_date(api, tweet['tweet_id'])
        if tweet_date:
            tweet['date'] = tweet_date
            full_tweets.append(tweet)
    write_full_tweet_csv("./output/full_backfill.csv", full_tweets)

