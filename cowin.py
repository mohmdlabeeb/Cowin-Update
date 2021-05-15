import requests
import re
from datetime import datetime
import json
from mailjet_rest import Client
import os
import notify2
from playsound import playsound
from time import time, sleep


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
    api_key = 'fd437d487713dfdb2d771fb4a35a9e9d'
    api_secret = 'f20f0224f9d15b0ce1f36b98d2ddfdcc'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
      'Messages': [
        {
          "From": {
            "Email": "updatecowin@gmail.com",
            "Name": "Update Cowin"
          },
          "To": [
            {
              "Email": email,
              "Name": name
            }
          ],
          "Subject": "Cowin vaccination center available",
          "TextPart": message,
          "HTMLPart": "<h3>STAY STRONG</h3><br>%s" %message,
          "CustomID": "AppGettingStartedTest"
        }
      ]
    }
    result = mailjet.send.create(data=data)
    print (result.status_code)
    print (result.json())

starttime = time()
pincode = get_pin()
centers = []
email = input("Please enter your email :\n")
date =  datetime.today().strftime('%d-%m-%Y')
while True:
    headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    response =  requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=%s&date=%s" % (pincode, date),headers=headers)
    print(response)
    json_dump = json.dumps(response.json())
    center_data = json.loads(json_dump)
    for center in center_data["centers"]:
        for session in center['sessions']:
            print(session['available_capacity'])
            if session['available_capacity'] >= 2:
                centers.append(center['name'])
                print(center['name'],center['address'],center['center_id'])
                notify2.init('Cowin')
                n = notify2.Notification('Vaccine available',centers)
                send_mail(email,centers)
                playsound('beep.mp3')
                playsound('beep.mp3')
                playsound('beep.mp3')
                playsound('beep.mp3')
                playsound('beep.mp3')
    sleep(30 - time() % 30)



