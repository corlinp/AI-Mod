import requests, json, os
from src.utils.db_connections import get_redis
from src.utils.secret_storage import secrets

"""

Contains utilities for checking the safety of the domain on Web of Trust

"""

api_key = secrets['wot_key']

bad_legend = {'101':"Malware or Virus", '102':'Bad Store', '103':'Phishing', '104':'Scam', '105':'Illegal Content'}
maybe_legend = {'201':'Unethical Site', '202':'Privacy Risk', '203':'Suspicious Site', '204':'Hate Website',
                '205': 'Spam', '206': 'Unwanted Downloads', '207': 'Popups'}

r = get_redis()


def check_domain(link, use_redis_caching=True):
    redis_name = 'domain_' + link
    # We're going to use Redis caching so we don't kill their API with imgur.com links
    try:
        if use_redis_caching and r.exists(redis_name):
            return json.loads(r.get(redis_name))
    except Exception as e:
        print(e)
        print("Unable to connect to Redis. Is it running?")

    api_url = "http://api.mywot.com/0.4/public_link_json2?hosts=%s/&callback=process&key=%s" % (link, api_key)
    res = requests.get(api_url)
    data = json.loads(res.text[8:-1])
    report = {'notes': [], 'spam': 0}
    to_check = list(data.values())[0]
    if 'categories' in to_check:
        for key, value in to_check['categories'].items():
            if key == '401':
                report['nsfw'] = value/100.0
            if key == '501':
                # If it's not GOOD it's probably something. We'll call it other.
                report['other'] = 1.0 - value/100.0
                if report['other'] > 0.4:
                    report['notes'].append("Questionable Website")
                pass
            if key in bad_legend:
                report['spam'] = value/100.0
                report['notes'].append(bad_legend[key])
            if key in maybe_legend:
                report['maybe'] = value/100.0
                report['notes'].append(maybe_legend[key])
    else:
        # This means it's not found
        report['notes'].append('Obscure Website')

    if link == 'goo.gl' or link == 'bit.ly':
        report['notes'].append('Link Shorteners')
        report['spam'] = 0.75

    # This will expire the WOT info in 72 hours (in case it does change or is never used again)
    if use_redis_caching:
        r.set(redis_name, json.dumps(report), ex=259200)

    return report

def delete_redis_cache():
    keys = r.keys('domain_*')
    for key in keys:
        print(key)
        r.delete(key)

if __name__ == "__main__":
    print(check_domain("bit.ly/sososo", True))
