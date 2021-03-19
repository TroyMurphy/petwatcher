from twilio.rest import Client
from decouple import config


def send_text(contents):
    print("Sample")


def send_real_text(contents):
    ac = config("TWILIO_AC", cast=str)
    key = config("TWILIO_KEY", cast=str)
    textFrom = config("TEXTFROM", cast=str)
    textTo = config("TEXTTO", cast=str)
    client = Client(ac, key)
    client.messages.create(to=textTo, from_=textFrom, body=contents)
