"""
This program will search Google for some exact phrase and return the total number of results.

The idea here is that if a google search for an address or phone number has a lot of results, it's public.

This will allow the doxing filter to tell the difference between someone posting a politicians's public phone number vs a person's private phone number.

"""
import re
import requests
from bs4 import BeautifulSoup

# Gets the search result count for a query (puts it in quotes)
def get_google_count(q):
    r = requests.get('http://www.google.com/search', params={'q': '"'+q+'"'})
    if "No results found for" in r.text:
        return 0
    soup = BeautifulSoup(r.text, 'lxml')
    val = soup.find('div',{'id':'resultStats'}).text
    val = int(re.findall(r'[0-9,]+', val)[0].replace(',', ''))
    return val

# Returns a coefficient of probability for whether or not the searched address is public or not
def is_public(text):
    num = get_google_count(text)
    return 1.0 - 1.0/(0.01 * num + 1.0)

if __name__ == '__main__':
    print(is_public('1600 Pennsylvania Ave')) # The white house's address
    print(is_public('5969 Lusk Blvd, San Diego, CA 92121')) # Address of a Chili's near UCSD
    print(is_public('4281 Nonsense Dr')) # Some random address
