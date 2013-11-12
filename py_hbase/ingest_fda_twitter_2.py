#!/usr/bin/env python
import requests
import os
import os.path
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import struct
import base64
import glob
import json

baseurl = "http://localhost:8080"

cfname = "messages"
messagecolumn = "message"

usernamecolumn = "username"
linenumbercolumn = "line"
username = "shakespeare"

linenumbercolumnencoded = base64.b64encode(cfname + ":" + linenumbercolumn)
messagecolumnencoded = base64.b64encode(cfname + ":" + messagecolumn)

# Method for encoding ints with base64 encoding
def encode(n):
    data = struct.pack("i", n)
    s = base64.b64encode(data)
    return s

# Method for decoding ints with base64 encoding 
def decode(s):
    data = base64.b64decode(s)
    n = struct.unpack("i", data)
    return n[0]

# Checks the request object to see if the call was successful
def issuccessful(request):
    if 200 <= request.status_code and request.status_code <= 299:
        return True
    else:
        return False

def create_xml_cell_body(row, column_encoded, text_body):
    cell = SubElement(row, 'Cell', column=column_encoded)
    cell.text = text_body

    return cell

# Delete table if it exists
#request = requests.get(baseurl + "/" + tablename + "/schema", headers={"Accept" : "application/json"})
#
#if issuccessful(request):
#    request = requests.delete(baseurl + "/" + tablename + "/schema", headers={"Accept" : "application/json"})
#
#    if issuccessful(request):
#        print "Deleted table " + tablename
#    else:
#        print "Errored out.  Status code was " + str(request.status_code) + "\n" + request.text
#
# Create Messages Table
#content =  '<?xml version="1.0" encoding="UTF-8"?>'
#content += '<TableSchema name="' + tablename + '">'
#content += '  <ColumnSchema name="' + cfname + '" />'
#content += '</TableSchema>'
#
#request = requests.post(baseurl + "/" + tablename + "/schema", data=content, headers={"Content-Type" : "text/xml", "Accept" : "text/xml"})
#
#if issuccessful(request):
#    print "Created table " + tablename
#else:
#    print "Errored out while creating table.  Status code was " + str(request.status_code) + "\n" + request.text
#    quit()


tweet_files = glob.glob1(source_dir, 'twitter_json*.txt')
tweet_num = 1
# use glob to get all the textfiles
for filename in tweet_files:

    twitter_json_file = open(os.path.join(source_dir, filename), "rb")
    tw_json = json.loads(twitter_json_file.read())

    cellset = Element('CellSet')

    linenumber = 0;

    row_key = str(tw_json['id']) + '-' + str(tw_json['created_at']) + '-' + str(tweet_num).zfill(8)
    row_key_encoded = base64.b64encode(row_key)

    row = SubElement(cellset, 'Row', key=row_key_encoded)

    for j_key in tw_json.keys():


        if j_key == 'text':
            continue

        try:
            body_text_encoded = base64.b64encode(tw_json[j_key].encode('utf8'))
        except:
            body_text_encoded = base64.b64encode(str(tw_json[j_key]))

        meta_column_encoded = base64.b64encode(meta_cf + ":" + j_key)

        # Add message cell

        # Add username cell
        
        cell = create_xml_cell_body(row, meta_column_encoded, body_text_encoded)

    tweet_num = tweet_num + 1
    text_column_encoded = base64.b64encode(text_cf + ":" + 'text')
    cell = create_xml_cell_body(row, text_column_encoded, base64.b64encode(tw_json['text'].encode('utf8')))
    # Submit XML to REST server
    request = requests.post(baseurl + "/" + tablename + "/fakerow", data=tostring(cellset), headers={"Content-Type" : "text/xml", "Accept" : "text/xml"})

    if issuccessful(request):
        print "Added messages for " + filename
    else:
        print "Errored out while loading data.  Status code was " + str(request.status_code) + "\n" + request.text
        quit()
