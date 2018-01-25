import re, string, csv
from src.utils.ai_utils import root_path
from src.utils.text_cleaner import stem_word


# def stem_word(word):
#     if not hasattr(stem_word, 'lem'):
#         stem_word.lem = WordNetLemmatizer()
#     return stem_word.lem.lemmatize(word, 'v')


def edits(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   # Only replacing vowels for now but some time you can do consonants too if you want
   replaces   = [a + c + b[1:] for a, b in splits for c in 'aeiouy' if b]
   inserts    = [a + c + b     for a, b in splits for c in string.ascii_lowercase]
   return set(deletes + transposes + replaces + inserts)

leet_replace = []
with open(root_path + 'src/classifiers/trolling/leet_translate.csv') as fil:
    reader = csv.reader(fil)
    for line in reader:
        leet_replace.append(line)


def normalize_leet(word):
    word = re.sub(r'(.)\1+', r'\1', word)
    word = word.replace('ph', 'f')
    out = ''
    for letter in word:
        if ord(letter) >= 33 and ord(letter) <= 127:
            letter = leet_replace[ord(letter)-33][2]
        out += letter
    return out

# Temporary Profanity dict until we get a real one installed
profanity = {'fuck': 2, 'bitch': 2, 'nigger': 4, 'faggot': 4, 'fag':3, 'cunt': 4, 'shit': 1}
leetprofanity = {normalize_leet(k): v for k, v in profanity.items()}
fuzzyprofanity = {}
for k, v in leetprofanity.items():
    for w in edits(k):
        w = normalize_leet(w)
        fuzzyprofanity[w] = v

# Delete legitimate words from profanity dicts
with open(root_path + 'data/download/corpus.txt') as f:
    ws = f.readlines()
    for w in ws:
        w = w.strip()
        if w in fuzzyprofanity:
            del fuzzyprofanity[w]
        if w in leetprofanity:
            del leetprofanity[w]

def detect_profanity(text):
    text = text.lower()
    text = re.sub(r'([^a-zA-Z0-9 ])+', '', text)
    text = text.split(' ')
    total_bad_score = 0.0

    def check_bad(w):
        leeted = normalize_leet(w)
        if w in profanity:
            return profanity[w]**2 / 16.0

        if leeted in leetprofanity:
            return leetprofanity[leeted]**2 / 24.0

        if leeted in fuzzyprofanity:
            return fuzzyprofanity[leeted]**2 / 30.0

        return 0

    for word in text:
        total_bad_score += check_bad(word)
        total_bad_score += check_bad(stem_word(word))


    prof_score = min(total_bad_score / len(text) * 8.0, 1.0)
    return {'troll': prof_score}


if __name__ == '__main__':
    print(leetprofanity)
    print(detect_profanity("what a n1g3r"))
