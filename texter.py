"""
Texts user and waits for their response. Prints response into console.

Allows user to text and see replies in python console. Loggs messages to log file and loads previous messages on start.
"""

import ast
import json
import time
import logging
import datetime

from flask import Flask, request, send_from_directory
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

LOG_FILE_PATH = '/root/messaging/messages.log'
TWILIO_PHONE_NUMBER = '+12064832427'

app = Flask(__name__)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(LOG_FILE_PATH)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

CURRENT_MESSAGE_LIST = list()
NEW_MESSAGES = False

@app.route('/<path:path>')
def mainPage(path):
    return send_from_directory('resources', path)

@app.route('/out', methods=['POST'])
def out():
    recipient = request.form['to']
    body = request.form['message']

    if recipient and body:
        account_sid = 'xxx'
        auth_token = 'xxx'
        client = Client(account_sid, auth_token)

        message = client.api.account.messages.create(
            to= '+1{0}'.format(recipient),
            from_= TWILIO_PHONE_NUMBER,
            body= body
        )

        messageData = {
            'status': 'SENT',
            'from': recipient,
            'message': body,
            'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        }

        log.info(json.dumps(messageData))
        CURRENT_MESSAGE_LIST.append(messageData)
        NEW_MESSAGES = True

        return 'Message: {0}'.format(json.dumps(messageData))

    else:
        return 'No message included with request'


@app.route('/sms', methods=['POST'])
def sms():
    # print 'GOT A SMS...'
    number = request.form['From']
    message_body = request.form['Body']

    messageData = {
        'status': 'RECEIVED',
        'from': number,
        'message': message_body,
        'timestamp': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    }

    log.info(json.dumps(messageData))
    CURRENT_MESSAGE_LIST.append(messageData)
    NEW_MESSAGES = True

    # print "NUMBER: {0}".format(number)
    # print "MESSAGE: {0}".format(message_body)

    return ''

    # resp = MessagingResponse()
    # resp.message('Hello {0}, you said: {1}'.format(number, message_body))
    # return str(resp)

@app.route('/hasNewMessages', methods=['GET'])
def hasNewMessages():
    new = NEW_MESSAGES
    NEW_MESSAGES = False
    return new

@app.route('/getCurrentMessages', methods=['GET'])
def currentMessages():
    # print 'Returning Current Messages...'
    # print 'Here they are: {0}'.format(json.dumps(CURRENT_MESSAGE_LIST))
    return json.dumps(CURRENT_MESSAGE_LIST)

@app.route('/getAllMessages', methods=['GET'])
def allMessages():
    conversation = list()

    with open(LOG_FILE_PATH, 'r') as logfile:
        for line in logfile:
            line = line.replace("u'","'")
            line = line.replace("'", '"')
            conversation.append(json.loads(line))

    return str(conversation)

@app.route('/getLastTimestamp', methods=['GET'])
def lastTimestamp():
    if not CURRENT_MESSAGE_LIST:
        with open(LOG_FILE_PATH, 'r') as logfile:
            pass
            # TODO UNFINISHED...



if __name__ == '__main__':
    app.run(debug=True)
