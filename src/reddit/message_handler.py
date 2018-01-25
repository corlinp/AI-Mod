from praw.models import Message
from utils.db_connections import get_reddit
from reddit.subreddit_config import add_sub
red = get_reddit()

def check_messages():
    for item in red.inbox.unread():
        if isinstance(item, Message):
            subject = item.subject

            # This should accept mod invitations
            if subject.startswith('invitation to moderate /r/'):
                sub = subject[26:].lower()
                try:
                    red.subreddit(sub).mod.accept_invite()
                    add_sub(sub)
                    print("     Accepted invite to join /r/%s!" % sub)
                except:
                    pass
                item.mark_read()

check_messages()
