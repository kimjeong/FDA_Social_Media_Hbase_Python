#!/usr/bin/python

import io
import sys
import time
from urllib2 import URLError
import twitter
import json
import oauth_login
import webbrowser
import requests
import os
import os.path
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import struct
import base64



if __name__ == '__main__':
    fh = open('news_tweets_10_22_2013_ver1.txt','r')
    fw = open('news_tweets_10_22_2013_ver2.txt','w')
 
    for line in fh:
        if (line.find('created_at') < 0):
#            ed_line = line.replace('\"}', '===')
#            ed_line = ed_line.replace('t\"', '!==')
#            ed_line = ed_line.replace('{\"', '$==')
#            ed_line = ed_line.replace(':\"', '#==')
#            ed_line = ed_line.replace('\"', '')
#            ed_line = ed_line.replace('===', '\"}')
#            ed_line = ed_line.replace('!==', 't\"')
#            ed_line = ed_line.replace('$==', '{\"')
#            ed_line = ed_line.replace('#==', ':\"')

            ed_line = line.replace('you\'ve','youve')
            ed_line = ed_line.replace('you\'d','youd')
            ed_line = ed_line.replace('you\'re','youre')
            ed_line = ed_line.replace('you\'ll','youll')
            ed_line = ed_line.replace('You\'ve','Youve')
            ed_line = ed_line.replace('You\'d','Youd')
            ed_line = ed_line.replace('You\'re','Youre')
            ed_line = ed_line.replace('You\'ll','Youll')
#        ed_line = ed_line.replace('t\"', 't')
#            ed_line = ed_line.replace('u\"\'', '1==')
#            ed_line = ed_line.replace('u\"','u\'')
            ed_line = ed_line.replace('u\'\'', '0==')
#            ed_line = ed_line.replace('\', ', '===')
            ed_line = ed_line.replace('u\'', '~==')
#            ed_line = ed_line.replace('\":', '')
#            ed_line = ed_line.replace('\':', '\":')
            ed_line = ed_line.replace('\\x', '')
#            ed_line = ed_line.replace('\", ', '^==')
#            ed_line = ed_line.replace('\', \'', '%==')
            ed_line = ed_line.replace('\"}', '-==')
            ed_line = ed_line.replace('text\":\"', '!==')
            ed_line = ed_line.replace('{\"', '$==')
#            ed_line = ed_line.replace(':\"', '#==')
#            ed_line = ed_line.replace('\":', '+==')
            ed_line = ed_line.replace('\"', '')
            ed_line = ed_line.replace('===', '\",')
            ed_line = ed_line.replace('\",\'','\", \"')
            ed_line = ed_line.replace('!==', 'text\":\"')
            ed_line = ed_line.replace('$==', '{\"')
            ed_line = ed_line.replace('#==', ':\"')
            ed_line = ed_line.replace('+==', '\":')
            ed_line = ed_line.replace('~==', '\"')      
            ed_line = ed_line.replace('%==', '\", \"')      
            ed_line = ed_line.replace('-==', '\"}')      
            ed_line = ed_line.replace('^==', '\", ')
            ed_line = ed_line.replace('===', '\", \"')      
            ed_line = ed_line.replace('0==', '\"\"')
            ed_line = ed_line.replace('1==', '\"')
            ed_line = ed_line.replace('\r', ' ')
#            ed_line = ed_line.replace('None', '\"None\"')
#            ed_line = ed_line.replace('False', '\"False\"')
#            ed_line = ed_line.replace('True', '\"True\"')
            ed_line = ed_line.replace('\n', ' ')

            fw.write(ed_line)
        else:
            fw.write(line)

    fh.close()
    fw.close()
