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
    fh = codecs.open('news_tweets_10_22_2013_ver2.txt','r','utf-8')
    data = json.load(fh)
    fh.close()

