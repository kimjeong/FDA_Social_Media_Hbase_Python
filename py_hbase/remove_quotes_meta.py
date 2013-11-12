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
import codecs



if __name__ == '__main__':
    fh = codecs.open('meta_tweets_10_15_2013.txt','r','utf-8')
    fw = codecs.open('meta_tweets_10_17_2013_ver1.txt','w','utf-8')
 
    for line in fh:
        ed_line = line.replace('you\'ve','youve')
        ed_line = ed_line.replace('you\'d','youd')
        ed_line = ed_line.replace('you\'re','youre')
        ed_line = ed_line.replace('you\'ll','youll')
        ed_line = ed_line.replace('You\'ve','Youve')
        ed_line = ed_line.replace('You\'d','Youd')
        ed_line = ed_line.replace('You\'re','Youre')
        ed_line = ed_line.replace('You\'ll','Youll')
#        ed_line = ed_line.replace('t\"', 't')
        ed_line = ed_line.replace('qu\'il', 'quil')
        ed_line = ed_line.replace('qu\'elle', 'quelle')
        ed_line = ed_line.replace('u\"\'', '1==')
        ed_line = ed_line.replace('u\"','u\'')
        ed_line = ed_line.replace('u\'\'', '0==')
        ed_line = ed_line.replace('\', ', '===')
        ed_line = ed_line.replace('u\'', '~==')
        ed_line = ed_line.replace('\":', '')
        ed_line = ed_line.replace('\':', '\":')
        ed_line = ed_line.replace('\\x', '')
        ed_line = ed_line.replace('\", ', '^==')
        ed_line = ed_line.replace('\', \'', '%==')
        ed_line = ed_line.replace('\'}', '-==')
        ed_line = ed_line.replace('text\":', '!==')
        ed_line = ed_line.replace('{\"', '$==')
        ed_line = ed_line.replace(':\"', '#==')
        ed_line = ed_line.replace('\":', '+==')
        ed_line = ed_line.replace('\"', '')
        ed_line = ed_line.replace('===', '\",')
        ed_line = ed_line.replace('\",\'','\", \"')
        ed_line = ed_line.replace('!==', 'text\":')
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
        ed_line = ed_line.replace('None', '\"None\"')
        ed_line = ed_line.replace('False', '\"False\"')
        ed_line = ed_line.replace('True', '\"True\"')
        if (ed_line.find('\"default_profile\"') < 0):
            ed_line = ed_line.replace('\n', '')
        fw.write(ed_line)

    fh.close()
    fw.close()
