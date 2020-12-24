import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def process_tweet():
    acct = 'jonasampath'
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '15'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    
    js = json.loads(data)
    
    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
    tweets = dict()
    for u in js['users']:
        print(u['screen_name'])
        if 'status' not in u:
            print('   * No status found')
            continue
        s = u['status']['text']
        tweets[u['screen_name']] = s[:600]
    return (tweets)
