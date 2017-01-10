import os
import sys
import requests
import json
import time
headers = {'Content-Type': 'application/json'}
import requests
from flask import Flask, request
moj_id=0;
app = Flask(__name__)


@app.route('/facebook/name', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        '''
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        '''
        return request.args["hub.challenge"], 200
	
    return "Hello world", 200


@app.route('/facebook/name', methods=['POST'])
def webhook():
     data = request.get_json()
     #try:
     #print data
     for entry in data["entry"]:
        for change in entry["changes"]:
            print change["value"]
            print change["value"].keys()
            #print change["value"].keys()[0]
            if change["value"].keys()[0]=="reaction_type" and str(change["value"]["reaction_type"])=="like"  and (str(change["value"]["verb"])=="add" or str(change["value"]["verb"])=="edit"):
                print str(change["value"]["reaction_type"]) 
                print str(change["value"]["sender_id"]) 
                print str(change["value"]["verb"]) 
                print "neko je lajkovao"
                print str(change["value"]["post_id"])



            '''
            for key in change["value"].keys():
                 print key
                 print "the key name is " + key + " and its value is " + str(change["value"][key])
             
            print change["value"][0]["reaction_type"]
            if "reaction_type" in change['value']:
               print "ovde sam"
               print change["value"][0]["reaction_type"]
            if "post_id" in change['value'][0]:
              print "ovde sam 2 "
              print change["value"][0]["post_id"]
            
            print "dolazim do ovde"
            print change["value"]["sender_id"]
      
            '''
     return "ok",200


if __name__ == '__main__':
    app.run(debug=True,port=80)
