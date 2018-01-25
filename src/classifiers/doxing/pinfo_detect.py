"""

This mostly contains a bunch of regex to detect personal info posted online. Still in development.

"""

import re
from src.classifiers.doxing.google_search_size import get_google_count


ip_adress_regex = re.compile(r"\b([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\b")
special_character_regex = re.compile(r"[^A-Za-z0-9\n]+")
number_regex = re.compile(r"([0-9]+)")

word_numbers = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'hundred': '00',
    'thousand': '000',
    }

public_area_codes = ['800', '888', '900']


def find_ip_addresses(text):
    out = []
    for match in re.findall(ip_adress_regex, text):
        if all([int(n) < 256 for n in match.split('.')]):
            out.append(match)
    return out


def find_phone_numbers(text):
    phone_numbers = []

    subbed = re.sub(special_character_regex, '', text).lower()
    for k, v in word_numbers.items():
        subbed = subbed.replace(k, str(v))
    matches = re.findall(number_regex, subbed)
    for number in matches:
        if number[0] == '1' and len(number) == 11:
            number = number[1:]
        if len(number) != 10:
            continue
        if number[:3] in public_area_codes:
            continue
        phone_numbers.append(number)

    return phone_numbers



if __name__ == '__main__':
    print(find_phone_numbers("dsasadsda! gg. call 1 [eight]00 867-5309 and 6197864114"))
    print(find_ip_addresses("my ip[ is 68.107.115.184 --- 77.424.55.2"))
