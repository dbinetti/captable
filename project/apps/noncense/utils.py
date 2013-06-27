from django.conf import settings

from random import randint
from twilio.rest import TwilioRestClient
from django.http import HttpResponse, HttpResponseNotFound

from django.views.decorators.csrf import csrf_exempt


import json


@csrf_exempt
def sendcode(mobile=None):
    ''' receives the request, and responds with code or error '''
    code = randint(1001, 9999)
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token  = settings.TWILIO_AUTH_TOKEN
    twilio_from = settings.TWILIO_FROM_NUMBER
    client = TwilioRestClient(account_sid, auth_token)
    message = client.sms.messages.create(to=mobile, from_=twilio_from, body="%s" % (code))
    twilio_response = dict(mobile=message.to, code=message.body, twilio_sid=message.sid)
    return twilio_response

# @csrf_exempt
# def logmein(request, mobile):
#     ''' receives the REST-formatted request, and responds with code or error '''
#     twilio_response = sendcode(mobile)
#     twilio_response = json.dumps(twilio_response)
#     return HttpResponse(twilio_response, content_type="application/json")
