import traceback
from src.classifiers.link.link_checker import scan_links
from src.classifiers.trolling.trolling_classifier import detect_trolling
from src.classifiers.spam.spam_classifier import detect_spam
from src.classifiers.trolling.profanity_detect import detect_profanity
from src.classifiers.trolling.perspectiveAPI import perspective
import copy

"""

This is the master method for checking some text against all of AI Mod's classifiers.
There will other methods for Reddit-specific ones like Flair and rulebreaking

'cheap' methods do not use long-running processes or limited / un-cacheable API calls.
    Use cheap=True when running bulk / fast analysis

"""
cheap_classifiers = [scan_links, detect_trolling, detect_spam, detect_profanity]
expensive_classifiers = [perspective]
empty_report = {'nsfw': 0, 'spam': 0, 'troll': 0, 'other': 0, 'notes': []}


debug_print_type = "none"

def analyze_text(text, cheap=False):
    if len(text) == 0:
        return copy.deepcopy(empty_report)

    final_results = []

    classifiers = cheap_classifiers
    if not cheap:
        classifiers += expensive_classifiers

    for method in classifiers:
        try:
            result = method(text)
            if debug_print_type in result:
                print(method.__name__ + ": " + str(result[debug_print_type]))
        except:
            traceback.print_exc()
            result = None
        if not isinstance(result, dict):
            print("There's something wrong with the results from %s: %s" % (method.__name__, str(result)))
        else:
            final_results.append(result)

    report = combine_reports(*final_results)
    # turn those decimals into nice integers
    for k, v in report.items():
        if isinstance(v, float):
            report[k] = int(round(v*100.0))

    return report


def combine_reports(*args):
    # if isinstance(args[0], list):
    #     args = args[0]
    master_dict = copy.deepcopy(empty_report) #{'notes': []}
    totals = empty_report.copy()
    for dic in args:
        for k, v in dic.items():
            if k in master_dict:
                if k == 'notes':
                    for note in v:
                        if note not in master_dict['notes']:
                            master_dict['notes'].append(note)
                else:
                    master_dict[k] += v**10
                    totals[k] += 1

    for k, v in totals.items():
        if k != 'notes' and v > 0:
            master_dict[k] = (master_dict[k] / v)**0.1

    return master_dict


def test(text):
    report = analyze_text(text, cheap=True)
    fixed = [text[:36]] + [str(report[p]) if p in report else '0' for p in parts[1:]]
    print('{0:40}{1:8}{2:8}{3:8}{4:8}{5:8}'.format(*fixed))


if __name__ == '__main__':
    parts = ['text','nsfw', 'spam', 'troll', 'other', 'notes']
    print('{0:40}{1:8}{2:8}{3:8}{4:8}{5:8}'.format(*parts))

    print('NSFW Comments')
    test("have you seen pornhub dot com? Best site")
    test("http://redtube.com/boobs is hottt")

    print('\nSpam Comments')
    test("Make money working from home.")
    test("FREE IPHONE 6S WHEN YOU SIGN UP")
    test("Online streaming site watch now")
    test("Free Shipping On Portable Phone Chargers!")
    test("OMG bit.ly/spamlink ;)")

    print('\nTroll comments')
    test("Suck my dick homo")
    test("You phuckng faget")
    test("Go die in a hole libtard")

    print('\nProfane comments')
    test("you fucking retarded bitch")
    test("you're a cunt")

    print('\nMisspelled Profanity')
    test("Fuucck you")
    test("You're a piece of sh1t")
    test("You dum Cun7 fckr")

    print('\nGood Comments')
    test("There are Linux distros under 15MB.")
    test("I used to have a dog just like him!")
    test("Pretty sure that's not safe to eat")
    test("Try out http://wolframalpha.com/")




