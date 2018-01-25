from src.utils.secret_storage import secrets
import os
import redis
import praw

"""
I really don't know if this is the right way to do this so someone stop me if it's not.

But here you'll find instances (like a connection pool) to connect to all out databases and shit.

"""

# We'd really like to know if this is running in docker so we can set the connections appropriately.
IN_DOCKER = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER')
if IN_DOCKER:
    print("IM RUNNING IN DOCKER")
else:
    print("IM NOT RUNNING IN DOCKER")


def get_redis():
    if not hasattr(get_redis, 'r'):
        if IN_DOCKER:
            get_redis.r = redis.StrictRedis(charset="utf-8", decode_responses=True, host='redis')
        else:
            get_redis.r = redis.StrictRedis(charset="utf-8", decode_responses=True)

    return get_redis.r


def get_reddit():
    if not hasattr(get_reddit, 'red'):
        get_reddit.red = praw.Reddit(**secrets['account'])

    return get_reddit.red
