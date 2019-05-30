# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

def send_sms(msg, outnumber):
    tw_number = '+15744062933'
    account_sid = 'AC993099d300c96b3d2da5d7d2e16b20f0'
    auth_token = '1c89b776e5139f956a1acea7ac7622ba'
    client = Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body=msg,
                     from_=tw_number,
                     to=outnumber
                 )
    return message.sid