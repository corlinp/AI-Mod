import json
from src.utils.ai_utils import root_path


try:
    with open(root_path + 'src/reddit/config/mod_status.json') as jf:
        subreddits = json.load(jf)
except:
    subreddits = []


def get_subs():
    return subreddits

def add_sub(sub):
    subreddits.append(sub)
    with open(root_path + 'src/reddit/config/mod_status.json', 'w') as jf:
        json.dump(subreddits, jf)


def get_config(sub):
    return SubConfig()


class SubConfig:
    """
    Provides configuration for different parts of the sub.
    Also starts off with a sort of default config
    """
    def __init__(self):
        self.leave_comment_on_removal = False
        self.removal_thresholds = {'troll': 95, 'spam': 95, 'nsfw': 95}
        self.report_thresholds = {'troll': 76, 'spam': 76, 'nsfw': 76}

    def to_json(self):
        out = {}
        for attr in vars(self):
            if attr is not None:
                out[attr] = getattr(self, attr)
        return json.dumps(out)

    def save(self):
        pass


if __name__ == "__main__":
    print(get_subs())
    add_sub('ucsd')
    print(get_subs())