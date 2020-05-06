import os
from darksky.api import DarkSky
from darksky.types import weather
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
import tweepy
import json
import time

# CONSTANTS
load_dotenv()
DARKSKY = os.getenv("d_token")
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


def get_lat_long(location_str: str):
    """
    Given a location  from Twitter, generate lat and long
    :param location_str: Name of location (Manhattan, Camelback Mountain, .etc)
    :return: lat, long tuple
    """
    geolocator = Nominatim(user_agent="urbanclimate")
    try:
        location = geolocator.geocode(location_str)
        return round(location.latitude, 4), round(location.longitude, 4)
    except Exception as e:
        print(e)
        return None


def get_hourly_weather_data(lat, long):
    """
    Given a location, get the weather data for the next 48 hrs.
    :param lat: latitude
    :param long: longitude
    :return: list of hourly weather data for the given lat long
    """
    darksky = DarkSky(DARKSKY)
    try:
        # get the data
        forecast = darksky.get_forecast(
            lat, long,
            exclude=[weather.CURRENTLY, weather.MINUTELY,
                     weather.DAILY, weather.ALERTS, weather.FLAGS])

        # add lat & long to the hourly weather data for composite key in db
        hourly_weather_data = []
        for data in forecast['hourly']['data']:
            data['latitude'] = lat
            data['longitude'] = long
            hourly_weather_data.append(data)

        # Lets save the weather data while were at it
        # for data in hourly_weather_data:
        #     db.weather_container.create_item(data)

        return hourly_weather_data
    except Exception as e:
        print(e)
        return None


def get_current_weather_data(lat, long):
    """
    Given a location, get the weather data for the next 48 hrs.
    :param lat: latitude
    :param long: longitude
    :return: list of hourly weather data for the given lat long
    """
    darksky = DarkSky(DARKSKY)
    try:
        # get the data
        forecast = darksky.get_forecast(
            lat, long,
            exclude=[weather.HOURLY, weather.MINUTELY,
                     weather.DAILY, weather.ALERTS, weather.FLAGS])

        # add lat & long to the hourly weather data for composite key in db
        data = forecast.currently
        data.latitude = lat
        data.longitude = long
        data = data.__dict__
        data.pop("time")
        return data
    except Exception as e:
        print(e)
        return None


def twitter_created_at_to_epoch(created_at):
    """
    Converts twitters created at to epoch time
    'Wed Oct 10 20:19:24 +0000 2018' -> 1539227964
    :param created_at:
    :return: epoch time as int
    """
    try:
        return int(time.mktime(time.strptime(
            created_at,"%a %b %d %H:%M:%S +0000 %Y")))
    except ValueError as e:
        print(f"something went wrong: {e}")
        return None


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
                    return False
            return True
    return False


if __name__ == "__main__":
    data = get_current_weather_data(33.7541, -116.8927)