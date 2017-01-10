#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import time
import sqlite3
import datetime
headers = {'Content-Type': 'application/json'}
import requests
from flask import Flask, request,render_template
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
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":
    

        for entry in data["entry"]:
            print entry
            for messaging_event in entry["messaging"]:


                if messaging_event.get("message"):
                    print messaging_event

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]
                    conn = sqlite3.connect('users2.db')
                    c = conn.cursor() 
                    try:
                     rezultat=messaging_event["message"]["quick_reply"]["payload"]
                     rezultat=rezultat.split("_")
                     anketeid=rezultat[0]
                     odgovor=rezultat[1]
                     print anketeid
                     print odgovor
                     t=(anketeid,str(sender_id),odgovor,)
                     c.execute("INSERT into ankete_log VALUES (?,?,?)", t)
                     conn.commit()
                     conn.close()
                     send_message(sender_id,"Hvala vam na odgovoru")
                    except:pass


            
                    if 'text' in messaging_event["message"]: # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text
                        message_text = message_text.lower()
                        conn = sqlite3.connect('users2.db')
                        c = conn.cursor()
                        t=(str(sender_id),)
                        print sender_id
                        c.execute('SELECT * FROM users WHERE fbid=?', t)
                        row=c.fetchone()
                        print row
                        if row is None:
                          r = requests.get('https://graph.facebook.com/v2.6/'+sender_id+'?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD') 
                          name=r.json()['first_name']+" "+r.json()['last_name'] 
                          gender=r.json()['gender']                       
                          t=(str(sender_id),str(name),str(gender),"")
                          c.execute("INSERT INTO users VALUES (?,?,?,?)", t)
                          conn.commit()
                          conn.close()
                     
                    
                        if message_text == "stranka" or message_text == "stranke":
                        
                            print("nasao sam stranke.")
                            r=requests.get('http://88.99.75.129/politicka-partija',headers=headers)
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
                    
                        if message_text[0:4] == "klub" or message_text[0:6] == "klubovi":
                            # do something
                            print("nasao sam stranke.")
                            r=requests.get('http://88.99.75.129/poslanicki-klub',headers=headers)
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

                        if message_text == "grad" or message_text == "gradovi":
                            # do something
                            print("nasao sam grad.")
                            print("nasao sam stranke.")
                            r=requests.get('http://88.99.75.129//grad',headers=headers)
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
                            r=requests.get('http://88.99.75.129/saziv',headers=headers)
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

                        if len(message_text.split(" vs ")) == 2:
                            poslanik1 = message_text.split(" vs ")[0]
                            poslanik2 = message_text.split(" vs ")[1]
                        
                            print poslanik1
                            print poslanik2
                            id1=0
                            id2=0
                            #try: 
                            #    t1= poslanik1.split(" ")[0] + " " + poslanik1.split(" ")[1] + " " + poslanik2.split(" ")[0] + " " + poslanik2.split(" ")[1]
                            #    x=1
                            #except:
                            #    x=0
                            r1=requests.get('http://88.99.75.129/poslanik?ime=' + poslanik1.split(" ")[0] + '%20' + poslanik1.split(" ")[1] ,headers=headers)
                            datas1 = r1.json()
                        
                            if 'error' in datas1.keys():
                                send_message(sender_id, unicode("Poslanik " + poslanik1.split(" ")[0] + " " + poslanik1.split(" ")[1] + " nije pronadjen."))
                            else:
                                id1=datas1.values()[0][0]['id']
                       
                            r2=requests.get('http://88.99.75.129/poslanik?ime=' + poslanik2.split(" ")[0] + '&prezime=' + poslanik2.split(" ")[1] ,headers=headers)
                            datas2 = r2.json()
                            if 'error' in datas2.keys():
                                send_message(sender_id, unicode("Poslanik " + poslanik2.split(" ")[0] + " " + poslanik2.split(" ")[1] + " nije pronadjen."))
                            else:
                                id2=datas2.values()[0][0]['id']

                            if id1!=0 and id2!=0:
                                send_message(sender_id, unicode("link http://88.99.75.129/uporedi-poslanike?poslanik1="+str(id1)+"&poslanik2="+str(id2)))

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
                                ime=args[1]
                                prezime = args[2]
                                r_ime = requests.get('http://88.99.75.129/poslanik?ime=' + ime + '%20' + prezime,headers=headers)
                                data = r_ime.json()
                                if 'error' in data.keys():
                                    send_message(sender_id, unicode("Poslanik nije pronadjen."))
                                else:
                                    id1=data.values()[0][0]['id']
                                    send_message(sender_id, unicode("link http://88.99.75.129/poslanik/"+str(id1)))
                            else:
                                send_message(sender_id, unicode("greska"))

                        if message_text[0:5] == "osoba":
                            print "usao sam u meksikanku"
                            args = message_text.split(" ")
                        
                            if len(args) == 3: 
                                print "asdasd"   
                                ime=args[1]
                                prezime=args[2]
                                r_ime = requests.get('http://88.99.75.129/osoba',headers=headers)
                                data = r_ime.json()
                                store = ""
                                for i in data['osobe']:
                                    print "usao sam u donji deo"
                                    if (ime.lower() == i['ime'].lower()) and (prezime.lower() == i['prezime'].lower()):
                                        send_message(sender_id, unicode("Link: http://5.9.127.172/osoba/" + str(i['id'])))
                            else:
                                send_message(sender_id, unicode("greska"))
                        if message_text[0:7] == "odprati":
                            print "brisanje"
                            conn = sqlite3.connect('users2.db')
                            c = conn.cursor()
                            t=(sender_id,)
                            c.execute('DELETE FROM users WHERE fbid=?', t)
                            conn.commit()
                            send_message(sender_id, unicode("Ispraznili smo listu pracenja"))
                        

                        if message_text[0:5] == "prati":
                            def pronadjiid(name,last_name):
                                    print name
                                    print last_name
                                    headers = {'Content-Type': 'application/json'}
                                    r = requests.get('http://www.istinomer.rs/api/akter?show=all',headers=headers)
                                    datas=r.json()

                                    #print datas
                                    for i in datas:
                                     if unicode(i['ime'].lower())==name and unicode(i['prezime'].lower())==last_name:
                                        return i['id']
                            print "usao sam u prati"
                            conn = sqlite3.connect('users2.db')
                            c = conn.cursor()
                            
                            args = message_text.split(" ")
                       

                            if len(args) == 3:
                                print "ovde sam ja"
                                akterid=pronadjiid(args[1],args[2])
                                print akterid
                                if akterid is not None:
                                  print "sinisa mali"
                                  t=(str(sender_id),)
                                  print sender_id
                                  c.execute('SELECT * FROM users WHERE fbid=?', t)
                                  row=c.fetchone()
                                  print row
                                  if row is None:
                                   r = requests.get('https://graph.facebook.com/v2.6/'+sender_id+'?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD') 
                                   name=r.json()['first_name']+" "+r.json()['last_name'] 
                                   gender=r.json()['gender']                       
                                   t=(str(sender_id),str(name),str(gender),str(akterid))
                                   c.execute("INSERT INTO users VALUES (?,?,?,?)", t)
                                   conn.commit()
                                   t=(str(akterid),)
                                   c.execute("SELECT * FROM akteri WHERE id=?", t)
                                   final=c.fetchone()
                                   print ("final je ovo"+final)
                                   if final is None:
                                        t=(str(akterid),args[1]+" "+args[2])
                                        c.execute("INSERT INTO akteri VALUES (?,?)", t)
                                        conn.commit()

                                   conn.close()
                                   send_message(sender_id,unicode("Pratim za vas"+args[1]+" "+args[2]))
                                  else:
                                    t=(str(sender_id),)
                                    c.execute("SELECT istinomerids FROM users where fbid=?", t)
                                    row=c.fetchone()
                                    t=(str(row[0])+':'+str(akterid),str(sender_id))
                                    c.execute("UPDATE users SET istinomerids=? WHERE fbid=?", t)
                                    conn.commit()
                                    t=(str(akterid),)
                                    c.execute("SELECT * FROM akteri WHERE id=?", t)
                                    final=c.fetchone()
                                    if final is None:
                                        t=(str(akterid),args[1]+" "+args[2])
                                        c.execute("INSERT INTO akteri VALUES (?,?)", t)
                                        conn.commit()

                                    conn.close()
                                    send_message(sender_id,unicode("Pratim za vas "+args[1]+" "+args[2]))

                                else:
                                     send_message(sender_id,unicode("Nismo uspeli da pronadjemo nikog sa takvim imenom"))


                    

                        if message_text[0:3] == "akt":     
                            text = ""     
                            print "Usao sam"     
                            args = message_text.split(" ")
                            print args    
                            if len(args) == 2:
                                print "usao sam ovde"         
                                r = requests.get('http://88.99.75.129/akt?kljucnaRec=' + unicode(args[1]), headers=headers)
                                podaci = r.json()
                                for i in podaci['akta']:
                                    if len(text+"ID: " + str(i['akt_id']) + "\nNaslov " + i['naslov'] + "\nLink: " + i['url'] + "\n") > 320:
                                        send_message(sender_id, unicode(text))
                                        text = ""
                                    else:
                                        text = text + "ID: " + str(i['akt_id']) + "\nNaslov: " + i['naslov'] + "\nLink: " + i['url'] + "\n"
                            else:
                                r = requests.get('http://88.99.75.129/akt', headers=headers)
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




@app.route('/istinomer_hook',methods=["POST"])
def istinomer():
   URL=request.form['URL']
   print URL
   conn = sqlite3.connect('users2.db')
   c = conn.cursor() 
   headers = {'Content-Type': 'application/json'}
   r = requests.get(URL,headers=headers)
   datas=r.json()
   print datas
   print datas[0]['id']
   akter=datas[0]['akter']
   naslov =datas[0]['naslov']
   akterid=datas[0]['akter_id']
   slika=datas[0]['slika']

   url="http://www.istinomer.rs/ocena/"+str(datas[0]['id'])
   print naslov
   print akterid
   t=("%:"+str(akterid)+"%",)
   for row in c.execute('SELECT fbid FROM users WHERE istinomerids LIKE ?',t):
           print row
           pusti_vest(naslov,str(row[0]),url,slika,str(datas[0]['id']),akter)

   return "OK"

def pusti_vest(naslov,fbid,url,slika,id,akter):
    print "pustio sam vest"
    params = {
        "access_token": "EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id":fbid
        },
        "message": {
            "attachment":{
            "type":"template",
            "payload":{
            "template_type":"generic",
            "elements":[
          {
            "title":naslov,
            "item_url":url,
            "image_url":slika,
            "subtitle":akter,
            "buttons":[
              {
                "type":"web_url",
                "url":url,
                "title":"View Website"
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


@app.route('/')
def show_index(): 
   conn = sqlite3.connect('users2.db')
   c = conn.cursor()
   c.execute("SELECT COUNT(*) FROM users")
   people=str(c.fetchone())[1]
   c.execute("SELECT COUNT(*) FROM users WHERE gender='male'")
   man=str(c.fetchone())[1]
   c.execute("SELECT COUNT(*) FROM users WHERE gender='female'")
   women=str(c.fetchone())[1]
   print people
   print man
   print women
   return render_template('index.html', people=people,man=man,women=women)

@app.route('/istinomer')
def istinomer_page():
   conn = sqlite3.connect('users2.db')
   c = conn.cursor()
   b=conn.cursor()
   personas=[]
   for row in c.execute('SELECT * FROM akteri'):
      print str(row[0])
      t=("%"+str(row[0])+"%",)
      print t
      b.execute("SELECT COUNT(*) FROM users WHERE istinomerids LIKE ?",t)
      #print (row[1]+"ima ovoliko"+str(b.fetchone()))
      broj=(b.fetchone()[0],)
      row=row+broj
      print row
      personas.append(row)

   print personas
   return render_template('istinomer.html',personas=personas)    

@app.route('/rezultati')
def rezultati():
    conn = sqlite3.connect('users2.db')
    c = conn.cursor()
    anketas=[]
    for row in c.execute('SELECT * FROM ankete'):
        anketas.append(row)
    print anketas
    return render_template('tables.html', anketas=anketas)

@app.route('/ankete')
def show_anketa():    
   return app.send_static_file('ankete.html')
@app.route('/anketa_id/<id>')
def anketa(id):
    print id
    odgovori=[]
    pitanja=[]
    conn = sqlite3.connect('users2.db')
    c = conn.cursor()
    t=(str(id),)
    c.execute("SELECT * FROM ankete WHERE id=?",t)
    anketa=c.fetchone()

    for x in range(3, 9):
        print str(anketa[x])
        print x
        pitanja.append(str(anketa[x]))
        t=(str(id),str(anketa[x]))
        c.execute("SELECT COUNT(*) FROM ankete_log WHERE id=? AND answer=?",t)
        odgovor=c.fetchone()
        print odgovor
        odgovori.append(odgovor)

    print odgovori
    return render_template('prikaz.html', odgovori=odgovori,pitanja=pitanja,naziv=anketa[1])
   
@app.route('/research',methods=['GET'])
def research():
   conn = sqlite3.connect('users2.db')
   c = conn.cursor()
   text=request.args.get("anketa")
   male=request.args.get("male")
   female=request.args.get("female")
   odgovor1=request.args.get("odgovor1")
   odgovor2=request.args.get("odgovor2")
   odgovor3=request.args.get("odgovor3")
   odgovor4=request.args.get("odgovor4")
   odgovor5=request.args.get("odgovor5")
   odgovor6=request.args.get("odgovor6")
   today = datetime.date.today()
   timestamp = int(time.time())
   if male=="true" and female=="true":
      gender="both"
   else: 
      if male=="true":
         gender="male"
      else:gender="female"

   t=(str(timestamp),text,gender,odgovor1,odgovor2,odgovor3,odgovor4,odgovor5,odgovor6,str(today))
   
   c.execute("INSERT INTO ankete VALUES (?,?,?,?,?,?,?,?,?,?)", t)
   conn.commit()
   print male
   print female
   odgovori=[]
   
   for x in xrange(1,7):
       buffera=request.args.get("odgovor"+str(x))
       if buffera!="":
        print "odgovor"+str(x)
        odgovori.append(buffera)

       pass
  
   print odgovori
   print len(odgovori)
   
   #odgovori[]
   print text
   if male=="true":
      t=("male",)
      for row in c.execute('SELECT fbid FROM users WHERE gender=?',t):
           print row
           salji_anketu(odgovori,text,str(row[0]),timestamp)

   if female=="true":
      t=("female",)
      for row in c.execute('SELECT fbid FROM users WHERE gender=?',t):
           print row
           salji_anketu(odgovori,text,str(row[0]),timestamp)
   
   return "ok"
  

def show_anketa():    
   return app.send_static_file('ankete.html')


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


def salji_anketu(odgovori,text,fbid,timestamp):
   ukupno=[]
   print "ovde sam"
   for x in range(0, len(odgovori)):
    odgovor={
    "content_type":"text",
        "title":str(odgovori[x]),
        "payload":str(timestamp)+"_"+odgovori[x],
        "image_url":"http://petersfantastichats.com/img/red.png"
        }
    ukupno.append(odgovor)
    print ukupno



   params = {
        "access_token": "EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD"
    }
   headers = {
        "Content-Type": "application/json"
    }
   data = json.dumps({
        "recipient": {
            "id":fbid
        },
        "message": {
            "text": text,
            "quick_replies":
            
        ukupno
      }
      }
        )
   print data
   print "ovo"
   r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
   print "ovo"

@app.route('/make_research', methods=['GET'])
def make_research():
   print "usao sam ovde"
   text=request.args.get("anketa")
   option1=request.args.get("opcija1")   
   option2=request.args.get("opcija2")
   print text
   print option1
   print option2
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
            "text": text,
            "quick_replies":
            [{
        "content_type":"text",
        "title":option1,
        "payload":"Da",
        "image_url":"http://petersfantastichats.com/img/red.png"

      },
      {
        "content_type":"text",
        "title":option2,
        "payload":"Ne",
        "image_url":"http://petersfantastichats.com/img/green.png"

      }
      ]
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
