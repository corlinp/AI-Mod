from src.reddit.comment_post_scanner import scan_comment
from src.reddit.comment_post_scanner import scan_submission
from src.reddit.comment_post_scanner import user_multiplier
from src.utils.db_connections import get_redis
from src.utils.ai_utils import confidence
import json, requests
from src.utils.db_connections import get_reddit

red = get_reddit()


def get_sub_karma(user, subreddit):
    user = user.lower()
    subreddit = subreddit.lower()
    redis_key = 'subkarma/'+user+'/'+subreddit
    if get_redis().exists(redis_key):
        return float(get_redis().get(redis_key))
    query = {
            "size": 0,
            "query": {
                "bool": {
                  "must": [
                    {
                      "match": {
                        "subreddit": subreddit
                      }
                    },
                    {
                      "match": {
                        "author": user
                      }
                    }
                  ]
                }
              },
              "aggs": {
                "karma": {
                  "sum": {
                    "field": "score"
                  }
                }
              }
            }
    res = requests.get('https://elastic.pushshift.io/_search', data=json.dumps(query))
    karma = res.json()['aggregations']['karma']['value']
    get_redis().set(redis_key, karma, ex=1800)
    return karma


def sub_karma_offset(user, subreddit):
    sub_karma = get_sub_karma(user, subreddit)
    if sub_karma < 0:
        return min(sub_karma / 100.0, 0.6)
    sub_ext = -0.333 + 20.0 / (sub_karma + 60.0)
    return sub_ext * 0.75


# Registers a user as bad news.
def register_user(name, reason, conf):
    info = {"username":name, "type":reason, "confidence":conf}
    get_redis().hset("badusers", name, json.dumps(info))


def scan_user(user):
    if isinstance(user, str):
        user = red.redditor(user)

    username = user.name.lower()
    # if get_redis().sismember('scannedusers', username):
    #     return None, 0
    # get_redis().sadd('scannedusers', username)

    multiplier = user_multiplier(user)

    troll = 0.0
    spam = 0.0
    total = 0.0

    for comment in user.comments.new(limit=100):
        report = scan_comment(comment, multiplier=multiplier, cheap=True)
        if report['troll'] > 50:
            troll += 1.0 + (report['troll'] - 50) * 0.01
        if report['spam'] > 50:
            spam += 1.0 + (report['spam'] - 50) * 0.01
        total += 1.0

    for submission in user.submissions.new(limit=100):
        report = scan_submission(submission, multiplier=multiplier, cheap=True)
        if report['troll'] > 50:
            troll += 1.0 + (report['troll'] - 50) * 0.01
        if report['spam'] > 50:
            spam += 1.0 + (report['spam'] - 50) * 0.01
        total += 1.0

    spam = min(spam, total)
    troll = min(troll, total)

    pct_troll = float(confidence(troll, (total-troll)**0.5))
    pct_spam = float(confidence(spam, (total-spam)**0.5))

    if total < 6:
        pct_spam *= 0.85
        pct_troll *= 0.85

    if pct_troll > 0.60:
        register_user(username, 'troll', pct_troll)
        return 'troll', pct_troll
    if pct_spam > 0.60:
        register_user(username, 'spam', pct_spam)
        return 'spammer', pct_spam

    return None, 0


if __name__ == '__main__':
    #print(sub_karma_offset('tornato7', 'datasets'))
    print(scan_user("tornato7"))
