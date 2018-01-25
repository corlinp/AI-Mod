from src.utils.text_cleaner import clean_text
import src.classifiers.sklearn_text_classifier as classifier
from src.utils.ai_utils import root_path


"""
    For classifying comments as trolling / not trolling. 84% accurate.
"""


def __train(test=False, save=True):
    import csv
    labels = []
    data = []
    with open(root_path + 'data/download/trolling_data.csv', encoding='utf-8') as fil:
        reader = csv.reader(fil)
        for line in reader:
            labels.append(line[0])
            data.append(line[1])

    if test:
        clf = classifier.TextClassifier(data, labels, fraction_test=0.25)
        clf.accuracy()
        print(clf.possibilities("fuck you and your house you whore"))
        print(clf.possibilities("we seem like a nice person"))
        print(clf.possibilities("I need to take a huge shit"))
        print(clf.possibilities("You're full of shit"))
    else:
        clf = classifier.TextClassifier(data, labels)

    print("Trained Trolling Model")

    if save and not test:
        clf.save_model('trolling_1')

    return clf

def __load():
    """
    Attempts to load a trained classifier, or if non exists, train one.
    """
    out = classifier.load_model('trolling_1')
    if out is None:
        out = __train(test=False, save=True)
    return out

def detect_trolling(text):
    if not hasattr(detect_trolling, 'clf'):
        # Try to load it
        detect_trolling.clf = __load()
    clf = detect_trolling.clf
    report = {}
    text = clean_text(text)
    result = clf.possibilities(text)
    report['troll'] = result[1][0]
    return report


if __name__ == "__main__":
    __train(test=True)
    print(detect_trolling("suck my dick!"))
