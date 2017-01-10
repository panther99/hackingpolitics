import requests
import json
headers = {'Content-Type': 'application/json'}
r = requests.get('http://5.9.127.172/politicka-partija',headers=headers)
datas=r.json()
print datas
for i in datas['politickePartije']:
    print i['id']
    print i['naziv']
r1=requests.get('http://5.9.127.172/poslanik?ime=' + "veroljub" + '%20' + "arsic" ,headers=headers)
datas1 = r1.json()
test=datas1.values()[0][0]['id']
print test
 #log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

params = {
        "access_token": "EAAUBpmWBIYsBANZCoIrlaJgNUxlFsodNdHD7T1J4uVsaIcbRqLay4rmvv6Qy9ZA9oVZBjtCb5kxmcBLrTVxkDHaluZC1Cvlb6LBkP2gVbINe3ZCeSIbdrv9W3odQOhr0zpMWsDWJf0JWpkw6YMSmsR7KrYHzWGYZBgz4p0DEGILQZDZD"
    }
headers = {
        "Content-Type": "application/json"
    }
data = json.dumps({
        "recipient": {
            "id":"1051154701634056"
        },
        "message": {
            "text": "sisaj ga",
            "quick_replies":
            [{
        "content_type":"text",
        "title":"Red",
        "payload":"super"
      },
      {
        "content_type":"text",
        "title":"Green",
        "payload":"strava"
      }
      ]
      }
      }
        )
r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)