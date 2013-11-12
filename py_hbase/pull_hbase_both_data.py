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

    request = requests.get(baseurl + "/" + tablename + "/*/ecig_meta_data:user", headers={"Accept" : "text/xml"})

    request_text = requests.get(baseurl + "/" + tablename + "/*/ecig_text_data:text", headers={"Accept" : "text/xml"})

    root = fromstring(request.text)
    root_t = fromstring(request_text.text)

# Go through every row passed back
    cfname = 'ecig_meta_data'
    cfname_text = 'ecig_text_data'
    tw_fh = open('meta_tweets_10_10_2013.txt','w')
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
    
             if columnname == cfname + ":" + 'user':
                 tw_text = base64.b64decode(cell.text)
                 tw_text = tw_text.replace('u\'','\"')
                 tw_text = tw_text.replace('\'','\"')
                 tw_text = tw_text.replace('None','\"None\"')
                 tw_text = tw_text.replace('True','\"True\"')
                 tw_text = tw_text.replace('False','\"False\"')
                 tw_fh.write(tw_text + ',\n')

             if columnname_t == cfname_text + ':' + 'text':
                 text_str = '{\"text\":\"'                     
                 tw_text_t = text_str + base64.b64decode(cell_t.text) + '\"}'
                 tw_fh.write(tw_text_t + ',\n')

             

    tw_fh.close()
