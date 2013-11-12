#!/usr/bin/python

import io
import sys
import time
import requests
import base64
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

    request = requests.get(baseurl + "/" + tablename + "/*/ecig_text_data:text", headers={"Accept" : "text/xml"})

    root = fromstring(request.text)

# Go through every row passed back
    cfname = 'ecig_text_data'
    tw_fh = open('key_tweets_10_10_2013.txt','w')
    for row in root:
         message = ''
         linenumber = 0
         username = ''

         row_key = base64.b64decode(row.get('key'))
    
         tw_fh.write(row_key + '==')
     # Go through every cell in the row
         for cell in row:
             columnname = base64.b64decode(cell.get('column'))

             if cell.text == None:
                 continue
    
             if columnname == cfname + ":" + 'text':
                 tw_text = base64.b64decode(cell.text)
             
             tw_fh.write(tw_text + '\n')

    tw_fh.close()
