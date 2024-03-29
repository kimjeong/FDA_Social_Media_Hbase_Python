#!/usr/bin/python

import io
import sys
import time
import requests
import base64
import json
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

if __name__ == '__main__':

    tablename = "ecig_providers_fda_twitter_table"
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

    request = requests.get(baseurl + "/" + tablename + "/*/providers_meta_data:created_at", headers={"Accept" : "text/xml"})

    request_text = requests.get(baseurl + "/" + tablename + "/*/providers_text_data:text", headers={"Accept" : "text/xml"})

    root = fromstring(request.text)
    root_t = fromstring(request_text.text)

# Go through every row passed back
    cfname = 'providers_meta_data'
    cfname_text = 'providers_text_data'
    tw_fh = open('news_tweets_10_22_2013_ver1.txt','w')
    for row, row_t in zip(root, root_t):
         message = ''
         linenumber = 0
         username = ''

         row_key = base64.b64decode(row.get('key'))
    
#         tw_fh.write(row_key + '==')
     # Go through every cell in the row
         for cell, cell_t in zip(row, row_t):
             columnname = base64.b64decode(cell.get('column'))
             columnname_t = base64.b64decode(cell_t.get('column'))

             if cell.text == None:
                 continue
#             cell_text = base64.b64decode(cell.text)

             # skip non "news" tweets
#             if columnname == (cfname + ":" + 'user'):
#                 if ((cell_text.find('759251') < 0) & (cell_text.find('51241574') < 0) & (cell_text.find('807095') < 0)):
#                     continue
             if columnname == (cfname + ':' + 'id_str'):
                 news_flag = False
                 id_str = base64.b64decode(cell.text)
                 if id_str == '759251':
                     news_flag = True
                 elif id_str == '51241574':
                     news_flag = True
                 elif id_str == '807095':
                     news_flag = True
                 elif id_str == '1652541':
                     news_flag = True
                 else:
                     continue

#             print 'got_here'
             if columnname == (cfname + ":" + 'created_at'):
                 tw_created_at = base64.b64decode(cell.text)
                 tw_fh.write('{\"created_at\":\"' + tw_created_at + '\"},\n')

             if (columnname_t == (cfname_text + ':' + 'text')):
                 text_str = '{\"text\":\"'                     
                 tw_text_t = text_str + base64.b64decode(cell_t.text) + '\"}'
                 tw_fh.write(tw_text_t + ',\n')

             

    tw_fh.close()
