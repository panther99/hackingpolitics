import os
import sys
import json

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
                    message_text.lower()

                    if str(message_text) == "stranka" or str(message_text) == "stranke":
                        # do something
                        print("nasao sam stranke.")
                    
                    if str(message_text) == "klub" or str(message_text) == "klubovi":
                        # do something
                        print("nasao sam klub.")

                    if str(message_text) == "grad" or str(message_text) == "gradovi":
                        # do something
                        print("nasao sam grad.")

                    if str(message_text) == "glasanje" or str(message_text) == "glasanja":
                        print("glasanje")

                    if str(message_text) == "istrazivanje" or str(message_text) == "istrazivanja":
                        print("istrazivanja")

                    if str(message_text) == "novo" or str(message_text) == "aktuelno":
                        print("novo")

                    if str(message_text) == "saziv" or str(message_text) == "sazivi":
                        print("saziv")

                    send_message(sender_id, "got it, thanks!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

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