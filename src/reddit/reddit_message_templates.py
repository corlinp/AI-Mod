import random

footer = "\n\n---\n\nI am a bot, and this action was performed automatically using fancy machine learning. See /r/ai_mod or [ai-mod.com](http://ai-mod.com/) for more info."

trolling_removal = "Hello, /u/{user}. I have removed your comment as possible trolling or harassment. If you think this is in error, please [message the mods](https://www.reddit.com/message/compose?to=%2Fr%2F{subreddit}). Thanks!" + footer

removal = "Hello, /u/{user}. I have removed this for possibly violating the subreddit rules. If you think this is in error, please [message the mods](https://www.reddit.com/message/compose?to=%2Fr%2F{subreddit}). I'm still in Beta so sorry for any inconvenience!" + footer


_greetings = ["What's up guys", "Hello humans", "Hey guys", "AI Mod here"]
_second_part = ["just a heads up,", "quick heads up,", "just FYI", "just checking in -", "just to let you know", "just letting you know"]
_last_part = ["Please confirm.", "Check it out if you get the chance.", "Do double check on that.", "Can you double check?"]
_goodbyes = ['Beep Boop!', 'Thanks!', 'Bot out.', 'Thanks.', 'Thx', 'X', '']

def removal_modmessage(link, confidence, type):
    out = "AI MOD: "
    out += random.choice(_greetings) + ', '
    out += random.choice(_second_part) + ' '
    confidence = round(int(confidence))
    out += "I removed [this post]({link}) as it's {confidence}% likely to be {type}. ".format(link=link, confidence=confidence, type=type)
    out += random.choice(_last_part) + ' '
    out += random.choice(_goodbyes)
    return out


def report(typ, confidence, notes):
    out = "Possible {typ} ({confidence:.2g}%)".format(typ=typ, confidence=confidence)
    if notes is not None and len(notes) > 0:
        out += ', notes: ' + ', '.join(notes)
    return out


if __name__ == '__main__':
    print(removal_modmessage('abc', 76.25, 'trolling'))