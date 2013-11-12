#!/usr/bin/python

import os
import sys
import twitter

from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

# Go to http://twitter.com/apps/new to create an app and get these items
# See also http://dev.twitter.com/pages/oauth_single_token

APP_NAME = 'Ecig_Analytics'
CONSUMER_KEY = 'UgbbGu8wDPcs2PWQH6jwg'
CONSUMER_SECRET = 'hGr0qyTDxdUvUomJ4iQnVVa13gRPnVUUPEuQJW1h9M'


def oauth_login_ecig(app_name=APP_NAME,
                consumer_key=CONSUMER_KEY, 
                consumer_secret=CONSUMER_SECRET, 
                token_file='out/twitter.ecig.oauth'):

    try:
        (access_token, access_token_secret) = read_token_file(token_file)
    except IOError, e:
        print >> sys.stderr, "Cannot get tokens"

    return twitter.Twitter(auth=twitter.oauth.OAuth(access_token, access_token_secret,
                           consumer_key, consumer_secret))

if __name__ == '__main__':

    oauth_login_ecig(APP_NAME, CONSUMER_KEY, CONSUMER_SECRET)
