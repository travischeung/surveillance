        
# import RPi.GPIO as GPIO
import time
# gmail stuff
import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/']
our_email = 'travis.cheung69@gmail.com'

def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)
# 428510535995-iourd0p4tcktps4hn3uf0mturvfp19qj.apps.googleusercontent.com

gmail_authenticate()

# get the Gmail API service
service = gmail_authenticate()

# creates the email itself
def build_message(destination, body):
    message = MIMEText(body)
    message['to'] = destination
    message['from'] = our_email
    message['subject'] = "Intruder Detected"
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination, obj, body, attachments=[]):
    return service.users().messages().send(
      userId="me",
      body=build_message(destination, obj, body, attachments)
    ).execute()

send_message(service, "travis.cheung69@gmail.com", "detected movement")


# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(2, GPIO.IN)         #Read output from PIR motion sensor
# GPIO.setup(3, GPIO.OUT)         #LED output pin
# while True:
#     i=GPIO.input(2)
#     if i==0:                 #When output from motion sensor is LOW
#         print ("No intruders"),i
#         GPIO.output(3, 0)  #Turn OFF LED
#         time.sleep(0.1)
#     elif i==1:               #When output from motion sensor is HIGH
#         print ("Intruder detected"),i
#         send_message(service, "travis.cheung69@gmail.com", "detected movement")
#         GPIO.output(3, 1)  #Turn ON LED
#         time.sleep(0.1)

    