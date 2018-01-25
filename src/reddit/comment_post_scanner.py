from src.text_analysis import analyze_text
from datetime import datetime

km = lambda t: 0.60 + 51.0 / (t + 70.0)
am = lambda a: 0.60 + 200.0 / (a + 272.0)

# TODO: Incorporate a user's total posts in a sub, time since their last activity, and how many of their posts have been removed before in a sub

def user_multiplier(user):
    """
    Users with lots of Karma / Account age will have a multiplier to make AI Mod go easier on them.
    Really noob users might have a positive multiplier.
    """
    total_karma = user.link_karma * 0.9 + user.comment_karma * 1.1
    account_age_days = (datetime.now() - datetime.fromtimestamp(user.created_utc)).days

    if total_karma < 0:
        karma_mult = 1.33 + abs(total_karma / 100.0)
    else:
        karma_mult = km(total_karma)
    age_mult = am(account_age_days)

    out = (karma_mult + age_mult) * 0.5

    # if subreddit is not None:
    #     out += sub_karma_offset(user.name, subreddit)

    return out


def adjust_for_multiplier(report, multiplier):
    report['troll'] *= ((multiplier - 1.0) * 0.55) + 1.0
    report['spam'] *= multiplier
    report['spam'] = max(report['spam'], report['other'] * multiplier)
    report['troll'] = min(report['troll'], 100)
    report['spam'] = min(report['spam'], 100)


def scan_comment(comment, multiplier=None, cheap=False):
    text = comment.body
    if multiplier is None:
        multiplier = user_multiplier(comment.author)

    report = analyze_text(text, cheap)
    adjust_for_multiplier(report, multiplier)

    return report


def scan_submission(submission, multiplier=None, cheap=False):
    text = submission.title
    text += ' ' + submission.domain
    if submission.selftext:
        text += ' ' + submission.selftext
    if multiplier is None:
        multiplier = user_multiplier(submission.author)

    report = analyze_text(text, cheap)
    adjust_for_multiplier(report, multiplier)

    return report


if __name__ == '__main__':
    from src.utils.db_connections import get_reddit
    comment = get_reddit().comment("dn73img")
    print(comment.body)
    print(scan_comment(comment, cheap=False))
