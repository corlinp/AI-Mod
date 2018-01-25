import numpy as np
import random, pickle, os
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn.linear_model
from sklearn import svm
import sklearn.calibration
from src.utils.ai_utils import root_path

def trunc(str, l=60):
    return str if len(str) < l else str[:l-2] + '..'

def load_model(name):
    fname = root_path + 'data/trained_models/' + name
    if not os.path.exists(fname + '.clf.skl') or not os.path.exists(fname + '.vec.skl'):
        return None
    with open(fname + '.clf.skl', 'rb') as infile:
        clf = pickle.load(infile)
    with open(fname + '.vec.skl', 'rb') as infile:
        vec = pickle.load(infile)
    out = TextClassifier(classifier=clf, vectorizer=vec)
    # print("Loaded Model: " + name)
    return out

class TextClassifier:
    def __init__(self, train_x=None, train_y=None, fraction_test=0.0, use_lemmatization=True, classifier=None, vectorizer=None):

        if classifier is not None:
            self.clf = classifier
            self.vectorizer = vectorizer
            return

        self.fraction_test = fraction_test

        # Split the data into training and testing data
        if self.fraction_test > 0:
            # Split the data into training and testing data
            num_test = int(len(train_y) * self.fraction_test)
            self.test_Y = np.array(train_y[:num_test])
            self.test_X = np.array(train_x[:num_test])

            train_y = np.array(train_y[num_test:])
            train_x = np.array(train_x[num_test:])

            print('Training Samples: %i' % len(train_x))
            print('Testing Samples: %i' % len(self.test_X))



        self.vectorizer = TfidfVectorizer(sublinear_tf=False,
                                          stop_words='english',
                                          strip_accents='ascii')

        """
        I'm commenting lemmatization out for now because
        A) It doesn't improve accuracy much
        B) It makes it more difficult to save the fitted vectorizer
        """
        # if use_lemmatization:
        #     lem = WordNetLemmatizer()
        #     analyzer = self.vectorizer.build_analyzer()
        #     def lem_words(doc):
        #         return [lem.lemmatize(w) for w in analyzer(doc)]
        #     self.vectorizer.analyzer = lem_words

        train_x_vec = self.vectorizer.fit_transform(train_x)


        #########################
        # Best Classifiers
        # MultinomialNB - 74% 0.002 sec
        # Passive Aggressive - 76% 0.006 sec
        # sklearn.linear_model.SGDClassifier - 77% 0.006 sec
        # CalibratedClassifierCV - 78%, 0.045 sec, Gives errors sometimes
        # LinearSVC - 79%, 0.01 sec
        #########################

        # I decided on LinearSVC because it's fast, consistent, and accurate
        # Here are some params that may improve it slightly:
        #   multi_class='crammer_singer'
        #   max_iter=10000
        #self.clf = sklearn.linear_model.SGDClassifier()
        svm_classifier = svm.LinearSVC()
        self.clf = sklearn.calibration.CalibratedClassifierCV(svm_classifier)
        self.clf.fit(train_x_vec, train_y)


    def save_model(self, name):
        """
        Allows the user to save a trained model
        :param name: The Filename to Use
        """
        with open(root_path + 'data/trained_models/' + name + '.clf.skl', 'wb') as outfile:
            pickle.dump(self.clf, outfile)
        with open(root_path + 'data/trained_models/' + name + '.vec.skl', 'wb') as outfile:
            pickle.dump(self.vectorizer, outfile)
        print("Saved Model: " + name)


    # Returns a sorted array of confidence:flair things
    def possibilities(self, strings, sort_by_score=False):
        if type(strings) is not list:
            strings = [strings]
        vectorized = self.vectorizer.transform(strings)
        score = self.clf.predict_proba(vectorized)
        try:
            out = [(score[0][i], self.clf.classes_[i]) for i in range(len(score[0]))]
        except:
            out = [(score[i], self.clf.classes_[i]) for i in range(len(score))]
        if not sort_by_score:
            out = sorted(out, key=lambda x: x[1])
        else:
            #sort by score
            out.sort(reverse=True)
        return out


    # Pass a string to this to classify it. Returns (classification)
    def classify(self, strings):
        if type(strings) is not list:
            strings = [strings]

        vectorized = self.vectorizer.transform(strings)
        return self.clf.predict(vectorized)[0]


    def accuracy(self):
        correct = 0.0
        for i in range(len(self.test_X)):
            pred = self.classify(self.test_X[i])
            if pred == self.test_Y[i]:
                correct += 1
        print("Got %i right out of %i"%(int(correct), len(self.test_X)))
        acc_total = correct / len(self.test_X)
        print(("\nClassification was %f%% accurate!" % (acc_total)))

        # Print some examples about how it classifies things
        print(("{: >6} {: >24} {: >24} {: >90}".format('conf','actual', 'predicted', 'text')))
        print(('-'*150))
        runs = 0
        while runs < 10:
            i = random.randrange(0,len(self.test_X))
            text_part = trunc(self.test_X[i].split('and')[0].replace(' question','?'), 85)
            cresult = self.classify(self.test_X[i])
            if cresult != self.test_Y[i]:
                confidence = 0#self.confidence(test_X[i])
                try:
                    print(("{:.3f} {: >24} {: >24} {: >90}".format(confidence, self.test_Y[i], cresult, text_part)))
                except:
                    pass
                runs += 1
        return (correct / len(self.test_X))
