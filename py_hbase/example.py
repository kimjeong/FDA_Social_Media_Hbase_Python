#!/usr/bin/python

import io
import sys
import time
from urllib2 import URLError
import twitter
import json
import oauth_login_ecig_providers
import webbrowser
import requests
import os
import os.path
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import struct
import base64



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

def search_2(t, keys, ret_dict, user_id_list):

    twitter_stream = twitter.TwitterStream(auth=t.auth) # Reference the self.auth parameter

    follow_str = ','.join(user_id_list)

    print follow_str
    stream = twitter_stream.statuses.filter(follow=follow_str)

    tablename = "ecig_providers_fda_twitter_table"
    meta_cf = 'providers_meta_data'
    text_cf = 'providers_text_data'
    baseurl = "http://localhost:8080"

 
    search_ctr = 1   
    tweet_num = 0
    for tweet in stream:
        cellset = Element('CellSet')
        
        row_key = str(tweet['id']) + '-' + str(tweet['created_at']) + '-' + str(tweet_num).zfill(8)
        row_key_encoded = base64.b64encode(row_key)

        row = SubElement(cellset, 'Row', key=row_key_encoded)
        for key in keys:
            if key == 'text':
                continue
            store_tweet_hbase(row, key, meta_cf, text_cf, tweet)            

        request = requests.post(baseurl + "/" + tablename + "/fakerow", data=tostring(cellset), headers={"Content-Type" : "text/xml", "Accept" : "text/xml"})
        tweet_num = tweet_num + 1

    return ret_dict

def search(t, q=None, max_batches=5, count=100):

    search_results = t.search.tweets(q=q, count=count)

    statuses = search_results['statuses']

    for _ in range(max_batches):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
            kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
            search_results = twitter_api.search.tweets(**kwargs)
            statuses += search_results['statuses']

    return statuses


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


def make_twitter_request(t, max_errors, user_id_list): 

    wait_period = 2
    error_count = 0
    search_ctr = 1
    file_name = '../data/twitter/tmp_json_data.txt'
    keys = ['contributors', 'truncated', 'text', 'in_reply_to_status_id', 'id', 'favorite_count', 'source', 'retweeted', 'coordinates', 'in_reply_to_screen_name', 'in_reply_to_user_id', 'retweet_count', 'id_str', 'favorited', 'user', 'geo', 'in_reply_to_user_id_str', 'lang', 'created_at', 'in_reply_to_status_id_str', 'place']    

    ret_dict = {}
    while True:
        try:

            search_results = search_2(t, keys, ret_dict, user_id_list)

            file_name = '../data/twitter/twitter_json_' + str(search_ctr) + '.txt'
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
    t = oauth_login_ecig_providers.oauth_login()
    ecig_provider_user_id = get_ecig_providers_user_id('../data/ecig_providers.txt')
    make_twitter_request(t, 3, ecig_provider_user_id)
