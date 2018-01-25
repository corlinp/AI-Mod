import json
from ..utils.db_connections import get_reddit
from ..reddit.subreddit_config import get_subs

'''
This is a work-in-progress utility
The idea is to scan modlogs of a subreddit and use that data to improve the classifiers.
'''


reddit = get_reddit()

for sub in get_subs():
    for log in reddit.subreddit(sub).mod.log(limit=None):
        entry = {}
        entry['subreddit'] = log.subreddit
        entry['body'] = log.target_body
        entry['title'] = log.target_title
        entry['id'] = log.target_fullname
        entry['action'] = log.action
        entry['details'] = log.details

        # The following are less important
        entry['mod'] = log._mod
        entry['created'] = log.created_utc
        entry['author'] = log.target_author

        # Now to do something with the modlogs
        print(json.dumps(entry))
