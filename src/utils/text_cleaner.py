from unidecode import unidecode
import re
import os

url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.IGNORECASE)

# only checks for known domains - this is the one currently in use
url_pattern2 = re.compile(r'(([a-zA-Z0-9.]*)([a-zA-Z0-9]{2,256})\.(com|net|biz|org|ca|ru|fr|uk|de|jp|us|ch|es|jobs|info|ly|gl)[-a-zA-Z0-9@:%_\+.~#?&//=]*)', re.IGNORECASE)

# Checks for domains with everything after
url_pattern3 = re.compile(r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*))')

def stem_word(word):
    if word.endswith('ing'):
        word = word[:-3]
    elif word.endswith('ers'):
        word = word[:-3]
    elif word.endswith('er'):
        word = word[:-2]
    elif word.endswith('ies'):
        word = word[:-3]
    elif word.endswith('es'):
        word = word[:-2]
    elif word.endswith('s'):
        word = word[:-1]
    return word


def extract_urls(x_string):
    x_string = x_string.lower()
    x_string = x_string.replace(' dot ', '.')
    x_string = x_string.replace('[dot]', '.')
    x_string = x_string.replace('(dot)', '.')
    urls = re.findall(url_pattern2, x_string)
    urls = [u[0] for u in urls]
    return urls


def clean_text(text, trunc=None):
    if trunc is not None:
        if trunc < len(text):
            text = text[0:trunc] + text[trunc:min(len(text), trunc + 100)].split(' ')[0]

    # Works out any encoding problems
    # x_string = x_string.encode('ascii', 'ignore').decode()
    try:
        text = unidecode(text)
    except:
        pass
    text = text.lower()
    # Removes HTML Tags
    text = re.sub(r'<(/?[a-zA-Z0-9])*>', '', text)
    # Removes unicode danglers
    text = re.sub(r'(\\x[a-zA-Z0-9]{2})', ' ', text)
    text = re.sub(r'(\\u[a-zA-Z0-9]{4})', ' ', text)
    text = text.replace('\\n', ' ').replace('\\r', ' ')

    # Remove username mentions
    text = re.sub(r'(@[a-zA-Z0-9_\-]+)', ' uname ', text)
    text = re.sub(r'(/u/[a-zA-Z0-9_\-]+)', ' ', text)

    # Poor man's way of including punctuation
    text = text.replace('?', ' qest ').replace('!', ' excl ')
    text = text.replace('.', ' ')
    text = text.replace("'", '')
    text = re.sub(r'([^\s\w]|_)+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text



if __name__ == '__main__':
    print(clean_text("An updated YouTube-8M, a video understanding challenge, and a CVPR workshop. Oh my! http://www.google.com/"))
    print(extract_urls("http://www.monsto.biz Wh,at poop dot com potatoes the| ff_http://ww2.code.google.com/hjj/%20poop.computer?tag=666 please exmpl.com "))
    print(clean_text("i really don't understand..\n\n... your point.\xa0 It seems that you are mixing apples and oranges."))
    print(extract_urls("http://i.imgur.com/poop.jpg"))
