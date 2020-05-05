import os

class CosmosClient:
    def __init__(self, endpoint=None, key=None):
        if not endpoint:
            endpoint = os.getenv("endpoint")
        if not key:
            key = os.getenv("key")