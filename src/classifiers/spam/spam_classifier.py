"""

Contains methods for training and retraining spam classifiers.

Possible / future features:
 - Make subreddit-specific spam classifiers by scanning modlogs

"""
import os, re
from src.utils.text_cleaner import clean_text, extract_urls
import src.classifiers.sklearn_text_classifier as classifier
from src.utils.ai_utils import root_path


# Note: Even with the condensed 250,000 sample dataset this takes ~10G of memory to train
def __train(test=False, save=True):
    import csv
    labels = []
    data = []
    # Ya know we're just gonna do both comments and posts in one
    with open(root_path + 'data/download/condensed_spam_data.csv', encoding='utf-8') as fil:
        reader = csv.reader(fil)
        for line in reader:
            labels.append(line[0])
            data.append(line[1])

    print("Loaded Comment Data")

    if test:
        clf = classifier.TextClassifier(data, labels, fraction_test=0.25)
        clf.accuracy()

    else:
        clf = classifier.TextClassifier(data, labels)

    print("Trained Spam Model")

    if save and not test:
        clf.save_model('spam_1')

    return clf


def __load():
    """
    Attempts to load a trained classifier, or if non exists, train one.
    """
    out = classifier.load_model('spam_1')
    if out is None:
        out = __train(test=False, save=True)
    return out


def detect_spam(text):
    if not hasattr(detect_spam, 'clf'):
        # Try to load it
        detect_spam.clf = __load()
    clf = detect_spam.clf
    report = {}
    text = clean_text(text)
    result = clf.possibilities(text)
    spamresult = result[1][0]

    # Also if it's too short to really tell anything...
    if len(text) < 35:
        spamresult *= 0.95
    if len(text) < 25:
        spamresult *= 0.85
    if len(text) <= 10:
        spamresult *= 0.85

    # Punish if there is no link. Who spams without a link?
    if len(extract_urls(text)) == 0:
        spamresult *= 0.925

    report['spam'] = spamresult
    return report


if __name__ == "__main__":
    #__train(True)
    print(detect_spam('WIN A FREE IPHONE 5'))
