import os
import pandas as pd
import time
from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from util.db_client import  DBClient

# CONSTANTS
load_dotenv()
DARKSKY = os.getenv("d_token")


def get_lat_long(location_str: str):
    """
    Given a location  from Twitter, generate lat and long
    :param location_str: Name of location (Manhattan, Camelback Mountain, .etc)
    :return: lat, long tuple
    """
    geolocator = Nominatim(user_agent="urbanclimate")
    try:
        location = geolocator.geocode("manhattan")
        return location.latitude, location.longitude
    except Exception as e:
        print(e)
        return None


def get_weather_data(lat, long, db:DBClient):
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
        for data in hourly_weather_data:
            db.weather_container.create_item(data)

        return hourly_weather_data
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
    except ValueError:
        return None


