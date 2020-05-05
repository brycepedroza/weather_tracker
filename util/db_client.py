import os
from azure.cosmos import exceptions, CosmosClient, PartitionKey


class DBClient:
    def __init__(self, endpoint=None, key=None):
        if not endpoint:
            endpoint = os.getenv("endpoint")
        if not key:
            key = os.getenv("key")
        self.WEATHER = "weather_data"
        self.TWEETS = "tweets"
        self.database_name = "urban_climate"
        self.client = CosmosClient(endpoint, key)
        self.database = self.client.get_database_client(self.database_name)
        self.weather_container = self.database.get_container_client(self.WEATHER)
        self.tweet_container = self.database.get_container_client(self.TWEETS)


