from random import randint

from twilio.rest import TwilioRestClient

from django.conf import settings


def sendcode(mobile):
    """Generates and sends nonce through twilio"""
    code = randint(1001, 9999)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_from = settings.TWILIO_FROM_NUMBER
    client = TwilioRestClient(account_sid, auth_token)
    try:
        message = client.sms.messages.create(
            to=str(mobile),
            from_=twilio_from,
            body="{code}".format(code=code))
    except:
        raise Exception("Twilio Unreachable")
    return {'mobile': message.to[-10:], 'nonce': message.body}
