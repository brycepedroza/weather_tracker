import calendar
import time
from fastapi import FastAPI
from util.db_client import DBClient
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")
db_client = DBClient()

origins = [
    "http://localhost",
    "http://localhost:8000"
    "http://localhost:4000"
    "http://api:8000",
    "http://api:4000",
    "http://app:8000",
    "http://app:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/filter")
async def get_tweets(lat: float, long: float, range: float = .05):
    """
    Given a point, find all tweets in the range around it
    """
    query = f"select * from c where " \
            f"c.latitude  >= {lat-range } and " \
            f"c.latitude  <= {lat+range}  and " \
            f"c.longitude >= {long-range} and " \
            f"c.longitude <= {long+range} "
    print(query)
    items = list(db_client.tweet_container.query_items(
        query=query,
        enable_cross_partition_query=True))
    print(len(items))

    return {
        "count": len(items),
        "tweets": items
    }


@app.get("/api/region")
async def recent_tweets(
    lat1:  float = 24.686952,
    long1: float = -126.210938,
    lat2:  float = 50.457504,
    long2: float = -66.708984
):
    """
    get a list all tweets in a region from the last 12 hours
    """
    curr_time = (calendar.timegm(time.gmtime()))
    twelve_hours_seconds = 43200
    twelve_hours_ago = curr_time - twelve_hours_seconds
    query = f"select * from c where " \
            f"c.latitude  >= {lat1} and " \
            f"c.latitude  <= {lat2}  and " \
            f"c.longitude >= {long1} and " \
            f"c.longitude <= {long2} and " \
            f"c.epoch >= {twelve_hours_ago}"
    items = list(db_client.tweet_container.query_items(
        query=query,
        enable_cross_partition_query=True))

    return {
        "count": len(items),
        "tweets": items
    }


@app.get("/api/all")
async def get_all_tweets():
    """
    get all tweets
    """
    query = f"select * from c"
    items = list(db_client.tweet_container.query_items(
        query=query,
        enable_cross_partition_query=True))

    return {
        "count": len(items),
        "tweets": items
    }
