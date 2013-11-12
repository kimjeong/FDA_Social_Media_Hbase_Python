#!/usr/bin/python

import io
import sys
import time
from urllib2 import URLError
import twitter
import json
import oauth_login_ecig
import webbrowser
import requests
import os
import os.path
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import struct
import base64



# See recipe__get_friends_followers.py for an example of how you might use 
# make_twitter_request to do something like harvest a bunch of friend ids for a user
# -*- coding: utf-8 -*-

def create_xml_cell_body(row, column_encoded, text_body):
    cell = SubElement(row, 'Cell', column=column_encoded)
    cell.text = text_body

    return cell


def store_tweet_hbase(row, j_key, meta_cf, text_cf, tw_json):

    try:
        body_text_encoded = base64.b64encode(tw_json[j_key].encode('utf8'))
    except:
        body_text_encoded = base64.b64encode(str(tw_json[j_key]))

    meta_column_encoded = base64.b64encode(meta_cf + ":" + j_key)

    cell = create_xml_cell_body(row, meta_column_encoded, body_text_encoded)

    text_column_encoded = base64.b64encode(text_cf + ":" + 'text')
    cell = create_xml_cell_body(row, text_column_encoded, base64.b64encode(tw_json['text'].encode('utf8')))
    # Submit XML to REST server

def search_2(t, keys, ret_dict, user_id_list):
# Query terms

    #Q = ','.join(sys.argv[1:])

#    Q = ','.join(search_list.split())
    Q = 'ecigarette,e-cigarette,ecig,e-cig,bull smoke,v2 cig,smokeless image,flu vaccine,flu shot,influenza vaccine,flu mist,quadrivalent,flushot,flumist'
    
#    t = oauth_login() # Returns an instance of twitter.Twitter
    twitter_stream = twitter.TwitterStream(auth=t.auth) # Reference the self.auth parameter

    # See https://dev.twitter.com/docs/streaming-apis
    stream = twitter_stream.statuses.filter(track=Q)

    # For illustrative purposes, when all else fails, search for Justin Bieber
    # and something is sure to turn up (at least, on Twitter)

    tablename = "ecig_fda_twitter_table"
    meta_cf = 'ecig_meta_data'
    text_cf = 'ecig_text_data'
    baseurl = "http://localhost:8080"

 
    search_ctr = 1   
    tweet_num = 48000
    for tweet in stream:
        cellset = Element('CellSet')

        try:
            row_key = str(tweet['id']) + '-' + str(tweet['created_at']) + '-' + str(tweet_num).zfill(8)
        except:
            continue
        row_key_encoded = base64.b64encode(row_key)

        if tweet['id'] in user_id_list:
            continue
        row = SubElement(cellset, 'Row', key=row_key_encoded)
        for key in keys:
            if key == 'text':
                continue
            try:
                store_tweet_hbase(row, key, meta_cf, text_cf, tweet)            
            except:
                continue

        try:
            request = requests.post(baseurl + "/" + tablename + "/fakerow", data=tostring(cellset), headers={"Content-Type" : "text/xml", "Accept" : "text/xml"})
        except:
            continue
        tweet_num = tweet_num + 1

#            ret_dict[key] = tweet[key]
#            print str(ret_dict[key])
#        file_name = '../data/twitter/twitter_json_' + str(search_ctr) + '.txt'
#        print file_name
#        with io.open(file_name, 'w', encoding='utf-8') as f:
#            f.write(unicode(json.dumps(ret_dict, ensure_ascii=False)))
#        search_ctr = search_ctr + 1

#    for tweet in stream:
#        print tweet['contributors']

    return ret_dict

def search(t, q=None, max_batches=5, count=100):

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = t.search.tweets(q=q, count=count)

    statuses = search_results['statuses']

    # Iterate through more batches of results by following the cursor
    for _ in range(max_batches):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
            # Create a dictionary from next_results, which has the following form:
            # ?max_id=313519052523986943&q=%23MentionSomeoneImportantForYou&include_entities=1
            kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
            search_results = twitter_api.search.tweets(**kwargs)
            statuses += search_results['statuses']

    return statuses


def make_twitter_request(t, max_errors, user_id_list): 

    # A nested function for handling common HTTPErrors. Return an updated value 
    # for wait_period if the problem is a 503 error. Block until the rate limit is 
    # reset if a rate limiting issue

    def handle_http_error(e, t, wait_period=2):

        if wait_period > 3600: # Seconds
            print >> sys.stderr, 'Too many retries. Quitting.'
            raise e

        if e.e.code == 401:
            print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
            return None

        if e.e.code in (502, 503):
            print >> sys.stderr, 'Encountered %i Error. Will retry in %i seconds' % \
                    (e.e.code, wait_period)
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period

        # Rate limit exceeded. Wait 15 mins. See https://dev.twitter.com/docs/rate-limiting/1.1/limits
        if e.e.code == 429: 
            now = time.time()  # UTC
            sleep_time = 15*60 # 15 mins
            print >> sys.stderr, 'Rate limit reached: sleeping for 15 mins'
            time.sleep(sleep_time)
            return 0

        # What else can you do?
        raise e

    wait_period = 2
    error_count = 0
    search_ctr = 1
    file_name = '../data/twitter/tmp_json_data.txt'
    tmp_twitter_json = {"contributors": '', "truncated": False, "text": ". @FDA requiring color changes to fentanyl patches to aid safety: http://t.co/cOSQfZgT4O #FDA #pharma", "in_reply_to_status_id": '', "id": 383044657112182784, "favorite_count": 0, "source": "<a href=\"http://www.hootsuite.com\" rel=\"nofollow\">HootSuite</a>", "retweeted": False, "coordinates": '', "entities": {"symbols": [], "user_mentions": [{"id": 271155634, "indices": [2, 6], "id_str": "271155634", "screen_name": "FdA", "name": "Frits den Akker"}], "hashtags": [{"indices": [89, 93], "text": "FDA"}, {"indices": [94, 101], "text": "pharma"}], "urls": [{"url": "http://t.co/cOSQfZgT4O", "indices": [66, 88], "expanded_url": "http://tinyurl.com/ostpgak", "display_url": "tinyurl.com/ostpgak"}]}, "in_reply_to_screen_name": '', "in_reply_to_user_id": '', "retweet_count": 0, "id_str": "383044657112182784", "favorited": False, "user": {"follow_request_sent": False, "profile_use_background_image": True, "default_profile_image": False, "id": 32666698, "verified": False, "profile_text_color": "333333", "profile_image_url_https": "https://si0.twimg.com/profile_images/1562769623/Screen_shot_2011-06-13_at_2.33.18_PM_normal.png", "profile_sidebar_fill_color": "DDEEF6", "entities": {"url": {"urls": [{"url": "http://t.co/UsW8TJd3VW", "indices": [0, 22], "expanded_url": "http://whitsellinnovations.com", "display_url": "whitsellinnovations.com"}]}, "description": {"urls": []}}, "followers_count": 272, "profile_sidebar_border_color": "C0DEED", "id_str": "32666698", "profile_background_color": "C0DEED", "listed_count": 10, "profile_background_image_url_https": "https://abs.twimg.com/images/themes/theme1/bg.png", "utc_offset": '', "statuses_count": 1636, "description": "Founder of medical writing firm, Whitsell Innovations, Robin is: mom of 4, triathlete, advocate for entrepreneurs and ethical business.", "friends_count": 199, "location": "Chapel HIll, NC", "profile_link_color": "0084B4", "profile_image_url": "http://a0.twimg.com/profile_images/1562769623/Screen_shot_2011-06-13_at_2.33.18_PM_normal.png", "following": False, "geo_enabled": True, "profile_background_image_url": "http://abs.twimg.com/images/themes/theme1/bg.png", "screen_name": "robinwhitsell", "lang": "en", "profile_background_tile": False, "favourites_count": 2, "name": "Robin Whitsell", "notifications": False, "url": "http://t.co/UsW8TJd3VW", "created_at": "Fri Apr 17 23:45:45 +0000 2009", "contributors_enabled": False, "time_zone": '', "protected": False, "default_profile": True, "is_translator": False}, "geo": '', "in_reply_to_user_id_str": '', "possibly_sensitive": False, "lang": "en", "created_at": "Thu Sep 26 01:45:37 +0000 2013", "in_reply_to_status_id_str": '', "place": '', "metadata": {"iso_language_code": "en", "result_type": "recent"}}
    keys = ['contributors', 'truncated', 'text', 'in_reply_to_status_id', 'id', 'favorite_count', 'source', 'retweeted', 'coordinates', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'retweet_count', 'id_str', 'favorited', 'user', 'geo', 'in_reply_to_user_id_str', 'lang', 'created_at', 'in_reply_to_status_id_str', 'place']    
#    keys = ['id']
#    keys = tmp_twitter_json.keys()

    print keys
    ret_dict = {}
    while True:
        try:
#            return twitterFunction(*args, **kwArgs)
#            search_results = search(t, q='FDA fda @fda @FDA #fda #FDA')
            search_results = search_2(t, keys, ret_dict, user_id_list)
#            search_json = json.loads(search_results)
#            print search_results
#            json.dumps(search_results)
#            return
            file_name = '../data/twitter/twitter_json_' + str(search_ctr) + '.txt'
            print file_name
#            with io.open(file_name, 'w', encoding='utf-8') as f:
#                f.write(unicode(json.dumps(search_results, ensure_ascii=False)))
            file_h = open(file_name,'w')
            file_h.write(unicode(json.dumps(search_results, ensure_ascii=False)))
            file_h.close()

            search_ctr = search_ctr + 1
            sleep_time = 40
            time.sleep(sleep_time)
            error_count = 0
        except twitter.api.TwitterHTTPError, e:
            error_count = 0
            wait_period = handle_http_error(e, t, wait_period)
            if wait_period is None:
                return
        except URLError, e:
            error_count += 1
            print >> sys.stderr, "URLError encountered. Continuing."
            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise

def get_ecig_providers_user_id(data_file_name):

    fh = open(data_file_name,'r')
    user_id_list = []
    for line in fh:
        user_id = line.split()[1]
        user_id_list.append(user_id)

    fh.close()
    return user_id_list

if __name__ == '__main__':
    t = oauth_login_ecig.oauth_login_ecig()
    ecig_provider_user_id = get_ecig_providers_user_id('../data/ecig_providers.txt')
    make_twitter_request(t, 3, ecig_provider_user_id)
