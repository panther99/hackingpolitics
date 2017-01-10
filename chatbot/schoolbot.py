#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import time
import sqlite3
import random
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

    # endpoint for processing incoming messaging events

    data = request.get_json()
    conn = sqlite3.connect('ucenici.db')
    c = conn.cursor()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"] 
                    if 'text' in messaging_event["message"]: # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text
                        message_text = message_text.lower()

                    
                        if message_text == "ocene" or message_text == "ocena":
                        
                            print("nasao sam ocene.")
                            r = requests.get('https://graph.facebook.com/v2.6/'+sender_id+'?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD')
                            name=r.json()['first_name']+r.json()['last_name']
                            t=(str(sender_id),)
                            print sender_id
                            c.execute('SELECT * FROM ucenici WHERE fbid=?', t)
                            row=c.fetchone()
                            print row[0]
                            t=(str(row[0]),)
                            c.execute('SELECT * FROM ocene WHERE id=?', t)
                            ocene=c.fetchone()
                            text="matematika: "+ocene[1]+"srpski"+ocene[2]
                            send_message(sender_id, unicode(text))
                                      
                        if message_text[0:9] == "aktiviraj":
                            print "usao sam ovde"
                            args = message_text.split(" ")
                            kod=args[1]
                            t=(kod,)
                            c.execute('SELECT id FROM ucenici WHERE kod=?',t)
                            row=c.fetchone
                            t=(sender_id,"0","0",kod,)
                            c.execute("UPDATE ucenici SET fbid=?, status=?,kod=? WHERE kod=?",t)
                            text="ulogavni ste"
                            conn.commit()
                            conn.close()
                            send_message(sender_id,unicode(text))



                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200
@app.route('/')
def show_index():    
   return app.send_static_file('index.html')

@app.route('/objavipracenje')
def objavi_pracenje():
   send_message(sender_id,unicode("Ovde saljem link"))

def send_message(recipient_id, message_text):

    #og("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": "EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


@app.route('/make_research', methods=['GET'])
def make_research():
   conn = sqlite3.connect('ucenici.db')
   c = conn.cursor()
   print "usao sam ovde"
   text=request.args.get("anketa")
   filter1=request.args.get("filter")
   if filter1:
      t=(filter1,)
      for row in c.execute('SELECT fbid FROM ucenici WHERE smer=?',t):
        print row
        send_message(row[0],unicode(text))    

   else:
     print text
   
     for row in c.execute('SELECT fbid FROM ucenici'):
        print row
        send_message(row[0],unicode(text))
     return "OK"

@app.route('/add', methods=['GET'])
def add():
    ime=request.args.get("ime")
    odeljenje=request.args.get("odeljenje")
    smer=request.args.get("smer")
    kod=request.args.get("kod")
    conn = sqlite3.connect('ucenici.db')
    c = conn.cursor()
    ajdi=random.randrange(100, 1000, 2)
    print odeljenje
    print smer
    t=(ajdi,ime,odeljenje,smer,"0",kod,"0")
    c.execute('INSERT INTO ucenici VALUES (?,?,?,?,?,?,?)', t)
    conn.commit()
    conn.close()
    return "OK"

  


@app.route('/pustivest', methods=['GET'])
def pusti_vest():
    print "pustio sam vest"
    params = {
        "access_token": "EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id":"1127564757313703"
        },
        "message": {
            "attachment":{
            "type":"template",
            "payload":{
            "template_type":"generic",
            "elements":[
          {
            "title":"Istina: Veći broj izdatih građevinskih dozvola u Srbiji",
            "item_url":"http://www.istinomer.rs/ocena/3623/Veci-broj-izdatih-gradjevinskih-dozvola-u-Srbiji",
            "image_url":"http://www.istinomer.rs/pictures/ocena/slika/ce8250fe9eabc0029f6dc1fcabebceb3.JPG",
            "subtitle":"Zorana Mihajlović istinomer:ocena",
            "buttons":[
              {
                "type":"web_url",
                "url":"http://www.istinomer.rs/ocena/3623/Veci-broj-izdatih-gradjevinskih-dozvola-u-Srbiji",
                "title":"View Website"
              },
              {
                "type":"postback",
                "title":"Pozitivno",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
              {
                "type":"postback",
                "title":"Negativno",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              }                        
            ]
          }
         ]
         }
        }
         }
      }
        )
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    return "ok"

@app.route('/pustivest2', methods=['GET'])
def pusti_vest2():
    print "pustio sam vest2"
    params = {
        "access_token": "EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id":"1127564757313703"
        },
        "message": {
            "attachment":{
            "type":"template",
            "payload":{
            "template_type":"generic",
            "elements":[
          {
            "title":"Pemunuto kosovo",
            "item_url":"nesto",
            "image_url":"https://upload.wikimedia.org/wikipedia/commons/1/1f/Flag_of_Kosovo.svg",
            "subtitle":"Kosovo u beleskama",
            "buttons":[
              {
                "type":"web_url",
                "url":"http://127.0.0.1/local/index.html",
                "title":"Vidi"
              },
              {
                "type":"postback",
                "title":"Pozitivno",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              },
              {
                "type":"postback",
                "title":"Negativno",
                "payload":"DEVELOPER_DEFINED_PAYLOAD"
              }                        
            ]
          }
         ]
         }
          }
         }
      }
        )
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    print "ok"
    return "ok"

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True,port=80)
