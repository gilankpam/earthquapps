''''
This program is just waiting tweet for spesific twitter account
then send the tweet to benstalk queue
'''

from twitter import *

import beanstalkc
import unicodedata
import config
import sys


def main():
    try:
        b = beanstalkc.Connection(
            host=config.BEANSTALK['HOST'], port=config.BEANSTALK['PORT'])
    except beanstalkc.SocketError:
        print "Error connect to beanstalk, make sure beanstalk is running"
        sys.exit()

    b.use('news')

    auth = OAuth(
        consumer_key=config.CUSTOMER_KEY,
        consumer_secret=config.CUSTOMER_SECRET,
        token=config.ACCESS_TOKEN_KEY,
        token_secret=config.ACCESS_TOKEN_SECRET
    )

    stream = TwitterStream(auth=auth)
    itarator = stream.statuses.filter(follow=config.TWITTER_ID)

    print "Waiting for tweet till forever"
    # Forever loop
    for t in itarator:
        try:
            # Convert unicode string to ascii string
            news = unicodedata.normalize(
                'NFKD', t['text']).encode('ascii', 'ignore')
            b.put(news)
            print news
        except KeyError:
            pass

if __name__ == "__main__":
    main()
