#!/usr/bin/env python
#from common import *
import json
import base64
import requests
import os
import os.path
import glob
from ordereddict import OrderedDict
from starbase import Connection


def issuccessful(request):
    if 200 <= request.status_code and request.status_code <= 299:
        return True
    else:
        return False


tablename = 'fda_twitter_table'
baseurl = 'ec2-174-129-50-11.compute-1.amazonaws.com'
#baseurl = 'localhost'
connection = Connection(host='127.0.0.1', port=8080)
table = connection.table(tablename)

connection.tables()
print str(table.exists())
print table.columns()
quit()
# Delete table if it exists
#request = requests.get(baseurl + "/" + tablename + "/schema")

#print str(request.text)
#if issuccessful(request):
#    print "Deleted table " + tablename
#else:
#    print "Errored out.  Status code was " + str(request.status_code) + "\n" + request.text
#quit()


# Create Messages Table
#content =  '<?xml version="1.0" encoding="UTF-8"?>'
#content += '<TableSchema name="fda_twitter_table">'
#content += '  <ColumnSchema name="fda_meta_data" />'
#content += '  <ColumnSchema name="fda_text_data" />'
#content += '</TableSchema>'

# This JSON may work for table creation, but I haven't tried it
# {"name":"test5", "column_families":[{
#>              "name":"columnfam1",
#>              "bloomfilter":true,
#>              "time_to_live":10,
#>              "in_memory":false,
#>              "max_versions":2,
#>              "compression":"", 
#>              "max_value_length":50,
#>              "block_cache_enabled":true
#>           }
#> ]}

#request = requests.post(baseurl + "/" + tablename + "/schema", data=content, headers={"Content-Type" : "text/xml", "Accept" : "text/xml"})
#
#if issuccessful(request):
#    print "Created table " + tablename
#else:
#    print "Errored out while creating table.  Status code was " + str(request.status_code) + "\n" + request.text
#    quit()


# Create a message  for every work of Shakespeare
source_dir = "../data/twitter/"
meta_cf = 'fda_meta_data'
text_cf = 'fda_text_data'

tweet_num = 1

tweet_files = glob.glob1(source_dir, 'twitter_json*.txt')
# use glob to get all the textfiles
for filename in tweet_files:
    twitter_json_file = open(os.path.join(source_dir, filename), "r")

    lineNumber = 0;

    rows = []
    jsonOutput = { 'Row' : rows }

    tw_json = json.loads(twitter_json_file.read())

    row_key = str(tw_json['id']) + '-' + str(tw_json['created_at']) + '-' + str(tweet_num).zfill(8)
    row_key_encode = base64.b64encode(row_key)

    json_output = {'Row' : rows}

    tw_text_encode = base64.b64encode(text_cf + ':' + 'text')

    tw_contributors_encode = base64.b64encode(meta_cf + ':' + 'contributors')
    tw_truncated_encode = base64.b64encode(meta_cf + ':' + 'truncated')
    tw_in_reply_to_status_id_encode = base64.b64encode(meta_cf + ':' + 'in_reply_to_status_id')
    tw_id_encode = base64.b64encode(meta_cf + ':' + 'id')
    tw_favorite_count_encode = base64.b64encode(meta_cf + ':' + 'favorite_count')
    tw_source_encode = base64.b64encode(meta_cf + ':' + 'source')
    tw_retweeted_encode = base64.b64encode(meta_cf + ':' + 'retweeted')
    tw_coordinates_encode = base64.b64encode(meta_cf + ':' + 'coordinates')
    tw_in_reply_to_screen_name_encode = base64.b64encode(meta_cf + ':' + 'in_reply_to_screen_name')
    tw_in_reply_to_user_id_encode = base64.b64encode(meta_cf + ':' + 'in_reply_to_user_id')
    tw_retweet_count_encode = base64.b64encode(meta_cf + ':' + 'retweet_count')
    tw_id_str_encode = base64.b64encode(meta_cf + ':' + 'id_str')
    tw_favorited_encode = base64.b64encode(meta_cf + ':' + 'favorited')
    tw_user_encode = base64.b64encode(meta_cf + ':' + 'user')
    tw_geo_encode = base64.b64encode(meta_cf + ':' + 'geo')
    tw_in_reply_to_user_id_str_encode = base64.b64encode(meta_cf + ':' + 'in_reply_to_user_id_str')
    tw_lang_encode = base64.b64encode(meta_cf + ':' + 'lang')
    tw_created_at_encode = base64.b64encode(meta_cf + ':' + 'created_at')
    tw_in_reply_to_status_id_str_encode = base64.b64encode(meta_cf + ':' + 'in_reply_to_status_id_str')
    tw_place_encode = base64.b64encode(meta_cf + ':' + 'place')
   

    
    tmp_text = tw_json['text']
    tmp_text = tmp_text.encode('utf8')
    tmp_source = tw_json['source']
    tmp_source = tmp_source.encode('utf8')
    table.insert(row_key,
        {
            'fda_meta_data': {'contributors': str(tw_json['contributors']),
            'truncated' : str(tw_json['truncated']) ,
            'in_reply_to_status_id' : str(tw_json['in_reply_to_status_id']),
            'id' : str(tw_json['id']),
            'favorite_count' : str(tw_json['favorite_count']),
            'source' : tmp_source,
            'retweeted' : str(tw_json['retweeted']),
            'coordinates' : str(tw_json['coordinates']),
            'in_reply_to_screen_name' : str(tw_json['in_reply_to_screen_name']),
            'in_reply_to_user_id' : str(tw_json['in_reply_to_user_id']),
            'retweet_count' : str(tw_json['retweet_count']),
            'id_str' : str(tw_json['id_str']),
            'favorited' : str(tw_json['favorited']),
            'user' : str(tw_json['user']),
            'geo' : str(tw_json['geo']),
            'in_reply_to_user_id_str' : str(tw_json['in_reply_to_user_id_str']),
            'lang' : str(tw_json['lang']),
            'created_at' : str(tw_json['created_at']),
            'in_reply_to_status_id_str' : str(tw_json['in_reply_to_status_id_str']),
            'place' : str(tw_json['place'])
            },
            'fda_text_data': {'text': tmp_text}
        }
    )
        
#    cell1 = OrderedDict([
#        ("key", row_key_encode),
#        ("Cell", 
#         [
#                { "column" : tw_contributors_encode, "$" : base64.b64encode(str(tw_json['contributors'])) }
#
#                { "column" : tw_truncated_encode, "$" : base64.b64encode(str(tw_json['truncated'])) },
#                { "column" : tw_in_reply_to_status_id_encode, "$" : base64.b64encode(str(tw_json['in_reply_to_status_id'])) },
#                { "column" : tw_id_encode, "$" : base64.b64encode(str(tw_json['id'])) },
#                { "column" : tw_favorite_count_encode, "$" : base64.b64encode(str(tw_json['favorite_count'])) },
#                { "column" : tw_source_encode, "$" : base64.b64encode(tmp_source) },
#                { "column" : tw_retweeted_encode, "$" : base64.b64encode(str(tw_json['retweeted'])) },
#                { "column" : tw_coordinates_encode, "$" : base64.b64encode(str(tw_json['coordinates'])) },
#                { "column" : tw_in_reply_to_screen_name_encode, "$" : base64.b64encode(str(tw_json['in_reply_to_screen_name'])) },
#                { "column" : tw_in_reply_to_user_id_encode, "$" : base64.b64encode(str(tw_json['in_reply_to_user_id'])) },
#                { "column" : tw_retweet_count_encode, "$" : base64.b64encode(str(tw_json['retweet_count'])) },
#                { "column" : tw_id_str_encode, "$" : base64.b64encode(str(tw_json['id_str'])) },
#                { "column" : tw_favorited_encode, "$" : base64.b64encode(str(tw_json['favorited'])) },
#                { "column" : tw_user_encode, "$" : base64.b64encode(str(tw_json['user'])) },
#                { "column" : tw_geo_encode, "$" : base64.b64encode(str(tw_json['geo'])) },
#                { "column" : tw_in_reply_to_user_id_str_encode, "$" : base64.b64encode(str(tw_json['in_reply_to_user_id_str'])) },
#                { "column" : tw_lang_encode, "$" : base64.b64encode(str(tw_json['lang'])) },
#                { "column" : tw_created_at_encode, "$" : base64.b64encode(str(tw_json['created_at'])) },
#                { "column" : tw_in_reply_to_status_id_str_encode, "$" : base64.b64encode(str(tw_json['in_reply_to_status_id_str'])) },
#                { "column" : tw_place_encode, "$" : base64.b64encode(str(tw_json['place'])) },
#        ])
#    ])

#    cell2 = OrderedDict([
#        ("key", row_key_encode),
#        ("Cell", 
#         [
#                { "column" : tw_text_encode, "$" : base64.b64encode(tmp_text) }
#        ])
#
#    ])

#    print str(cell1)
#    rows.append(cell1)
#    rows.append(cell2)

    tweet_num = tweet_num + 1

    # Submit JSON to REST server
#    request = requests.post(baseurl + "/" + tablename + "/" + row_key, data=json.dumps(json_output), headers={"Content-Type" : "application/json", "Accept" : "application/json"})

#    if issuccessful(request):
#        print "Added messages for " + filename
#    else:
#        print "Errored out while loading data.  Status code was " + str(request.status_code) + "\n"

    twitter_json_file.close()
