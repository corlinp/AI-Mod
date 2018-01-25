from src.utils.text_cleaner import extract_urls
from src.utils.ai_utils import combine_reports_max
from src.classifiers.link.wot_checker import check_domain
import requests

whitelist = {'imleagues.com', 'kaggle.com', 'imgur.com',
             'i.imgur.com', 'example.com', 'shadertoy.com', 'youtube.com', 'youtu.be'}

greylist = {'amazon.com'}


def scan_links(text):
    urls = extract_urls(text)
    scanned_urls = []
    for url in urls:
        domain = stem_url(url)
        if domain not in whitelist:
            if domain in greylist:
                result = {'notes': [], 'spam': 0.60}
                if "amazon.com" in url and "tag=" in url:
                    result['spam'] = 0.96
                    result['notes'].append("Amazon Affiliate Link")
            else:
                result = check_domain(domain, use_redis_caching=True)

            if is_image(url):
                result['spam'] /= 5

            scanned_urls.append(result)

    out = combine_reports_max(*scanned_urls)
    if 'spam' not in out:
        out['spam'] = 0
    return out


def is_image(link):
    try:
        h = requests.head(link)
        header = h.headers
        content_type = header.get('content-type')
        return str(content_type).startswith('image')
    except:
        return False


def stem_url(link):
    link = link.lower()
    if link.startswith('http://'):
        link = link[7:]
    if link.startswith('https://'):
        link = link[8:]
    if link.startswith('www.'):
        link = link[4:]
    if '/' in link:
        link = link[:link.find('/')]
    if '.' not in link:
        print(str(link) + " is not a link!")
        return None
    return link


if __name__ == "__main__":
    print(scan_links("shadertoy.com"))
    print(scan_links("yahoo.com pornhub.com bit.ly/34533"))
    print(scan_links('https://i.imgur.com/mwwdFTZ.jpg'))
    print(scan_links('https://amazon.com/mwwdFTZ.jpg?tag=poop'))
