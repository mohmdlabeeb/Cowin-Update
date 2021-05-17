import requests
import re
from datetime import datetime
import json
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mailjet_rest import Client
import os
from playsound import playsound
from time import time, sleep

CLIENT_SECRET = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET,API_NAME,API_VERSION,SCOPES)

def get_pin():
    pincode = input("Please enter your pincode :\n")
    valid = isValidPinCode(pincode)
    if not valid:
        print("Please enter a valid pincode ")
        get_pin()
    return pincode
  
# Function to validate the pin code of India. 
# https://www.geeksforgeeks.org/how-to-validate-pin-code-of-india-using-regular-expression/
def isValidPinCode(pinCode):
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"; 
    p = re.compile(regex);
    if (pinCode == ''):
        return False;
    m = re.match(p, pinCode);
    if m is None:
        return False
    else:
        return True

def send_mail(email,centers):
    if centers:
        centers = ",".join(centers)
    else:
        centers = " "
    name = email.split("@")[0]
    message = "Vaccines availabe at %s" % centers
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = email
    mimeMessage['subject'] = 'Vaccine centre available'
    mimeMessage.attach(MIMEText(message, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()


starttime = time()
pincode = get_pin()
centers = []
email = input("Please enter your email :\n")
date =  datetime.today().strftime('%d-%m-%Y')
i = 0 
while True:
    i += 1
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    response =  requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=%s&date=%s" % (pincode, date),headers=headers)
    print(response)
    print(pincode)
    print("==========RUNNING %s============" %i)
    json_dump = json.dumps(response.json())
    center_data = json.loads(json_dump)
    for center in center_data["centers"]:
        for session in center['sessions']:
            print(session['available_capacity'])
            if session['available_capacity'] >= 2:
                centers.append(center['name'])
                print(center['name'],center['address'],center['center_id'])
                send_mail(email,centers)
                playsound('beep.mp3')
                playsound('beep.mp3')
                playsound('beep.mp3')
                playsound('beep.mp3')
                playsound('beep.mp3')
    sleep(30 - time() % 30)



