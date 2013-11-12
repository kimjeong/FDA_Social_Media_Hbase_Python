#!/usr/bin/python

import io
import sys
import time
import requests
import base64
import json
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

if __name__ == '__main__':

    tablename = "ecig_fda_twitter_table"
    baseurl = "http://localhost:8080"

#    tw_fh = open('ecig_tweets.txt','w')
#    request = requests.get(baseurl + "/" + tablename + "/*/ecig_text_data:text", headers={"Content-Type":"text/xml","Accept" : "text/xml"})

#    print str(request)
#    rows_data = request.text
#    print rows_data

#    for row in rows_data:
#        print row
#        tw_text = base64.b64decode(row.get('column')).encode('utf8')
#            
#        row_key = base64.b64decode(row.get('key'))
#
#        tw_fh.write(row_key + '==' + tw_text)
#
#    tw_fh.close()

    request = requests.get(baseurl + "/" + tablename + "/*/ecig_meta_data:user", headers={"Accept" : "application/json"})

#    request_text = requests.get(baseurl + "/" + tablename + "/*/ecig_text_data:text", headers={"Accept" : "application/json"})

    root = json.loads(request.text)
#    root_t = json.loads(request_text.text)

    cf_name = 'ecig_meta_data'
    message_column = 'user'

    for row in root['Row']:
        
#        for cell in row['Cell']:

         cell = row['Cell']
         column_name = base64.b64decode(cell['@column'])
         value = cell['$']

         if value == None:
             continue

         if column_name == (cf_name + ':' + message_column):
             message = base64.b64decode(value)
#             message_json = json.loads(message)
             print message
#    fh = open('ecig_meta_data_10_17_2013_ver1.txt','w')
#    fh_t = open('ecig_text_data_10_17_2013_ver1.txt','w')

#    json.dump(root, fh)
#    json.dump(root_t, fh_t)

#    fh.close()
#    fh_t.close()
