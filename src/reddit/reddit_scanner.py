import praw, json, re, time, traceback
import src.reddit.reddit_message_templates as templates
import logging
from src.reddit.subreddit_config import get_config, get_subs
from src.reddit.comment_post_scanner import scan_comment, scan_submission
from src.reddit.user_scanner import sub_karma_offset
from src.reddit.user_scanner import scan_user, user_multiplier
import src.utils.db_connections
from src.utils.discord_util import send_text

red = src.utils.db_connections.get_reddit()
r = src.utils.db_connections.get_redis()


# Determines whether or not we care about a comment
def take_action_or_no(comment):
    logging.debug("Checking Comment...")
    if comment.id in scanned:
        return False
    # If the comment was approved ignore it
    if comment.approved_at_utc is not None:
        return False
    logging.debug('past 1')
    # If I already reported it ignore it
    for report in comment.mod_reports:
        if report[1] == 'ai_mod':
            return False
    logging.debug('past 2')

    # # Ignore the comment if it was already removed
    if comment.banned_by is not None:
        return False
    logging.debug('past 3')

    # If I made the comment ignore it
    if comment.author.name == 'ai_mod':
        return False
    logging.debug('past 4')

    # If I can't mod it, ignore it
    if not comment.can_mod_post:
        return False
    logging.debug('past 5')

    return True

def print_report(link, report):
    parts = ['nsfw', 'spam', 'troll', 'other', 'notes', 'link']
    if not hasattr(print_report, 'printed'):
        print('{0:8}{1:8}{2:8}{3:8}{4:28}{5:50}'.format(*parts))
        print_report.printed = True

    fixed = [str(int(round(report[p]))) if p in report else '0' for p in parts[:-2]] + [str(report['notes'])] + [link]
    print('{0:8}{1:8}{2:8}{3:8}{4:28}{5:50}'.format(*fixed))


def log_action(link, reason, report, action, subreddit, karma_offset, multiplier):
    if isinstance(report, float):
        conf = report
        report = None
    else:
        conf = report[reason]
    out = {'link': link, 'reason': reason, 'conf': conf, 'action': action, 'time': int(time.time()), 'subreddit': subreddit}
    out = json.dumps(out)
    conf = round(int(conf))
    text = '[**'
    if action == 'report':
        text += 'Reported '
    elif action == 'remove':
        text += 'Removed '
    elif action == 'scan':
        text += 'Scanned '
    text += reason.title() + '**]('+link+') '
    text += '(' + str(conf) + r'%)'
    text += ' in /r/'+subreddit
    if report:
        if len(report['notes']) > 0:
            text += "\nNotes: " + ', '.join(report['notes'])
    text += "\nSubreddit Karma Offset: " + str(karma_offset)
    text += "\nUser Reputation Multiplier: " + str(multiplier)

    send_text(text)
    print(text)
    r.lpush('scanlog', out)
    r.ltrim('scanlog', 0, 24)


def start_scan():
    scan_comments(50)
    while True:
        scan_comments()
        time.sleep(5)


scanned = set()

def scan_comments(size = 10):
    """
    Indefinitely scan every monitored subreddit for new posts. Take action on those new posts when required.
    :return: 
    """
    posts = list(red.subreddit('+'.join(get_subs())).comments(limit=size*2))
    posts += list(red.subreddit('+'.join(get_subs())).new(limit=size))

    for comment in posts:
        sub = comment.subreddit.display_name.lower()
        cfg = get_config(sub)
        try:
            user = comment.author.name
            if isinstance(comment, praw.models.reddit.comment.Comment):
                link = comment.link_permalink + '' + comment.id + '/'
            else:
                link = 'https://www.reddit.com' + comment.permalink

            # If it was approved we don't need to do anything.
            if take_action_or_no(comment):
                multiplier = user_multiplier(comment.author)
                if isinstance(comment, praw.models.reddit.comment.Comment):
                    report = scan_comment(comment)
                else:
                    report = scan_submission(comment)

                scanned.add(comment.id)

                print_report(link, report)
                to_scan = ['troll', 'spam', 'nsfw']
                needs_scanning = False
                karma_offset = 0

                for typ in to_scan:
                    if report[typ] >= cfg.report_thresholds[typ]:
                        karma_offset = sub_karma_offset(user, sub)
                        report['troll'] += karma_offset * 100
                        report['spam'] += karma_offset * 100
                        break

                for typ in to_scan:
                    if report[typ] >= cfg.removal_thresholds[typ]:
                        if cfg.leave_comment_on_removal:
                            comment.reply(templates.removal.format(user=user, subreddit=sub))
                        comment.report(templates.report(typ, report[typ], report['notes']))
                        log_action(link, typ, report, 'remove', sub, karma_offset, multiplier)
                        comment.subreddit.message('AI Mod Removal',
                                                  templates.removal_modmessage(link, report[typ], typ))
                        comment.mod.remove()
                        needs_scanning = True
                        break

                    if report[typ] >= cfg.report_thresholds[typ]:
                        comment.report(templates.report(typ, report[typ], report['notes']))
                        log_action(link, typ, report, 'report', sub, karma_offset, multiplier)
                        needs_scanning = True
                        break

                if needs_scanning:
                    typ, rat = scan_user(comment.author)
                    if rat != 0:
                        print('Possible %s user: %s, %f rating' % (typ, user, rat))
                        log_action('https://www.reddit.com/user/'+user, typ, rat, 'scan', sub, karma_offset, multiplier)

        except Exception as e:
            print(e)
            traceback.print_exc()


if __name__ == '__main__':
    start_scan()
