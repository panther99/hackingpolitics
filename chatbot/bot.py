#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import time
headers = {'Content-Type': 'application/json'}
import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/facebook/name', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/facebook/name', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    message_text = message_text.lower()

                    
                    if message_text == "stranka" or message_text == "stranke":
                        
                        
                        print("nasao sam stranke.")
                        r=requests.get('http://5.9.127.172/politicka-partija',headers=headers)
                        datas=r.json()
                        print datas
                        text=""
                        textlen = 0
                        for i in datas['politickePartije']:
                            if len(text+str(i['id'])+"."+i['naziv']+"\n") > 320:
                                send_message(sender_id, unicode(text))
                                text = ""
                            else:
                                text = text+str(i['id'])+"."+i['naziv']+"\n"
                        '''
                        print len(text)
                        duzina=len(text)
                        puta=duzina/ 320
                        puta=round(puta)
                        print puta
                        for x in range(0, int(puta)):
                            od=int(x*320)
                            do=int(320*(x+1))
                            print od
                            print ("do ovog broja"+str(do))
                            text[int(od):int(do)]
                            send_message(sender_id, unicode(text[od:do]))
                            time.sleep(1)
                        '''

                    
                    
                    if message_text[0:4] == "klub" or message_text[0:6] == "klubovi":
                        # do something
                        print("nasao sam stranke.")
                        r=requests.get('http://5.9.127.172/poslanicki-klub',headers=headers)
                        datas=r.json()
                        #print datas
                        text=""
                        textlen = 0
                        args = message_text.split(" ")
                        query = ""
                        for arg in range(1, len(args)):
                            query = query + " " + args[arg]
                            print query
                        #print args[1].lower()
                        try:
                         t=args[1]
                         test=1
                        except IndexError:
                           print 'sorry, no 5'
                           test=0    
                        for i in datas['poslanickiKlub']:
                            if test==1:
                                print "postoji drugi argument"
                                #send_message(sender_id, unicode("imam drugi argument"))
                                print query

                                if unicode(i['naziv'].lower()).find(unicode(query.lower())) > -1:
                                        #send_message(sender_id, unicode("poklopio sam"))
                                    print("naso")
                                    if len(text+str(i['id'])+"."+i['naziv']+"\n"+"link: http://5.9.127.172/poslanicki-klub/"+str(i['id'])+"\n") > 320:
                                        send_message(sender_id, unicode(text))
                                    else:
                                        text = text+str(i['id'])+"."+i['naziv']+"\n"+"link: http://5.9.127.172/poslanicki-klub/"+str(i['id'])+"\n"
                                        send_message(sender_id, unicode(text))
                                        text = ""
                            else:
                                print "ja ulazim ovde"
                                if len(text+str(i['id'])+"."+i['naziv']+"\n"+"link: http://5.9.127.172/poslanicki-klub/"+str(i['id'])+"\n") > 320:
                                    send_message(sender_id, unicode(text))
                                    text = ""
                                else:
                                    text = text+str(i['id'])+"."+i['naziv']+"\n"+"link: http://5.9.127.172/poslanicki-klub/"+str(i['id'])+"\n"
                        '''
                        if len(text+str(i['id'])+"."+i['naziv']+"\n"+"link: http://5.9.127.172/poslanicki-klub/"+str(i['id'])+"\n") > 320:
                            send_message(sender_id, unicode(text))
                            text = ""
                        else:
                            text = text+str(i['id'])+"."+i['naziv']+"\n"+"link: http://5.9.127.172/poslanicki-klub/"+str(i['id'])+"\n"
                        '''

                    if message_text == "grad" or message_text == "gradovi":
                        # do something
                        print("nasao sam grad.")
                        print("nasao sam stranke.")
                        r=requests.get('http://5.9.127.172/grad',headers=headers)
                        datas=r.json()
                        print datas
                        text=""
                        for i in datas['mesta']:
                            text=text+str(i['id'])+"."+i['naziv']+"\n"
                        print len(text)
                        duzina=len(text)
                        puta=duzina/ 320
                        puta=round(puta)
                        print puta
                        for x in range(0, int(puta)):
                            od=int(x*320)
                            do=int(320*(x+1))
                            print od
                            print ("do ovog broja"+str(do))
                            text[int(od):int(do)]
                            send_message(sender_id, unicode(text[od:do]))
                            time.sleep(0.5)


                    if message_text == "glasanje" or message_text == "glasanja":
                        print("glasanje")

                    if message_text == "istrazivanje" or message_text == "istrazivanja":
                        print("istrazivanja")

                    if message_text == "novo" or message_text == "aktuelno":
                        print("novo")

                    if message_text == "saziv" or message_text == "sazivi":
                        print("saziv")
                        print("nasao sam grad.")
                        print("nasao sam stranke.")
                        r=requests.get('http://5.9.127.172/saziv',headers=headers)
                        datas=r.json()
                        print datas
                        text=""
                        textlen = 0
                        for i in datas["sazivi"]:
                            text=text+str(i['id'])+"."+i['naziv']+"\n"+"datum:"+i['od']+"\n"+"link: http://5.9.127.172/saziv/"+str(i['id'])+"\n"
                            textlen = textlen + len(text)
                            if textlen > 320:
                                send_message(sender_id, unicode(text))
                                text = ""
                            send_message(sender_id, unicode(text))
                            text = ""
                        '''
                        print len(text)
                        duzina=len(text)
                        puta=duzina / 320
                        puta=round(puta)
                        print puta
                        for x in range(0, int(puta)+1):
                            od=int(x*320)
                            do=int(320*(x+1))
                            print od
                            print ("do ovog broja"+str(do))
                            text[int(od):int(do)]
                            send_message(sender_id, unicode(text[od:do]))
                            time.sleep(0.5)
                        '''

                    if len(message_text.split(" vs ")) == 2:
                        poslanik1 = message_text.split(" vs ")[0]
                        poslanik2 = message_text.split(" vs ")[1]
                        
                        print poslanik1
                        print poslanik2
                        id1=0
                        id2=0
                        try: 
                            t1= poslanik1.split(" ")[0] + " " + poslanik1.split(" ")[1] + " " + poslanik2.split(" ")[0] + " " + poslanik2.split(" ")[1]
                            x=1
                        except:
                            x=0
                        r1=requests.get('http://5.9.127.172/poslanik?ime=' + poslanik1.split(" ")[0] + '%20' + poslanik1.split(" ")[1] ,headers=headers)
                        datas1 = r1.json()
                        
                        if 'error' in datas1.keys():
                            send_message(sender_id, unicode("Poslanik " + poslanik1.split(" ")[0] + " " + poslanik1.split(" ")[1] + " nije pronadjen."))
                        else:
                            if len(datas1) == 1:
                                id1=datas1.values()[0][0]['id']
                                print id1
                            else:
                                send_message(sender_id, unicode("Doslo je do greske: pokusajte biti precizniji."))
    
                        r2=requests.get('http://5.9.127.172/poslanik?ime=' + poslanik2.split(" ")[0] + '&prezime=' + poslanik2.split(" ")[1] ,headers=headers)
                        datas2 = r2.json()
                        if 'error' in datas2.keys():
                            send_message(sender_id, unicode("Poslanik " + poslanik2.split(" ")[0] + " " + poslanik2.split(" ")[1] + " nije pronadjen."))
                        else:
                            if len(datas2) == 1:
                              id2=datas2.values()[0][0]['id']
                              print id2
                            else:
                                send_message(sender_id, unicode("Doslo je do greske: pokusajte biti precizniji."))

                        if id1!=0 and id2!=0:
                           send_message(sender_id, unicode("link http://5.9.127.172/uporedi-poslanike?poslanik1="+str(id1)+"&poslanik2="+str(id2)))

                    else:
                        #send_message(sender_id, unicode("Morate uneti tekst u formatu: ime prvog poslanika vs ime drugog poslanika"))
                        pass
                        
                         
                    if message_text[0:8] == "poslanik":
                        pass
                        
                        args = message_text.split(" ")
                        try:
                            t1=args[1]+args[2]
                            test=1
                        except:
                            test=0
                        
                        if test==1:
                            '''

                            if args[1]=="stranka":
                              query=""
                              try:
                                t1=args[2]
                                b=1
                              except:b=0
                              if b==1:   
                                stanka = args[2]
                                print "sada sam usao u stranku"
                                for arg in range(2, len(args)):
                                   query = query + " " + args[arg]
                                   query=unicode(query)
                                print query
                                r=requests.get('http://5.9.127.172/poslanicki-klub',headers=headers)
                                datas=r.json()
                                for i in datas['poslanickiKlub']:
                                    if i[naziv].find(query)>0:
                                      id1=i['id']
                                      break
                            '''    
                            ime=args[1]
                            prezime = args[2]
                            r_ime = requests.get('http://5.9.127.172/poslanik?ime=' + ime + '%20' + prezime,headers=headers)
                            data = r_ime.json()
                            if 'error' in data.keys():
                                send_message(sender_id, unicode("Poslanik nije pronadjen."))
                            else:
                              id1=data.values()[0][0]['id']
                              send_message(sender_id, unicode("link http://5.9.127.172/poslanik/"+str(id1)))
                        else:
                            send_message(sender_id, unicode("greska"))
                        #r_ime = requests.get('http://5.9.127.172/poslanik?ime=' + ime + '%20' + prezime,headers=headers)
                        #data = r_ime.json()
                        #if 'error' in data.keys():
                            #send_message(sender_id, unicode("Poslanik nije pronadjen."))
                        #else:
                           #id1=data.values()[0][0]['id']
                           #send_message(sender_id, unicode("link http://5.9.127.172/poslanik/"+str(id1)))
                        '''

                        if args[3] == "u" and len(args) == 4:
                            ime = args[1]
                            prezime = args[2]
                            stranka = args[4]

                            r_ime = request.get('http://5.9.127.172/poslanik?ime=' + ime + '%20' + prezime)
                            poslanik = r_ime.json()
                            if 'error' in poslanik.keys():
                                send_message(sender_id, unicode("Poslanik " + ime + " " + prezime + " ne postoji."))
                        
                        else:
                            send_message(sender_id, unicode("Morate uneti tekst u formatu: poslanik ime prezime u stranka"))
                        '''

                    if message_text[0:3] == "akt":     
                        text = ""     
                        print "Usao sam"     
                        args = message_text.split(" ")
                        print args    
                        if len(args) == 2:
                            print "usao sam ovde"         
                            r = requests.get('http://5.9.127.172/akt?kljucnaRec=' + unicode(args[1]), headers=headers)
                            podaci = r.json()
                            for i in podaci['akta']:
                                if len(text+"ID: " + str(i['akt_id']) + "\nNaslov " + i['naslov'] + "\nLink: " + i['url'] + "\n") > 320:
                                    send_message(sender_id, unicode(text))
                                    text = ""
                                else:
                                    text = text + "ID: " + str(i['akt_id']) + "\nNaslov: " + i['naslov'] + "\nLink: " + i['url'] + "\n"
                        else:
                            r = requests.get('http://5.9.127.172/akt', headers=headers)
                            podaci = r.json()
                            for i in podaci['akta']:
                                if len(text + "ID: " + str(i['akt_id']) + "\nNaslov: " + i['naslov'] + "\nLink: " + i['url'] + "\n") > 320:
                                    send_message(sender_id, unicode(text))
                                    text = ""
                                else:
                                    text = text + "ID: " + str(i['akt_id']) + "\nNaslov: " + i['naslov'] + "\nLink: " + i['url'] + "\n"



                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


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


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True,port=8000)
