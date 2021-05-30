import requests
import re
from datetime import datetime
import json
from mailjet_rest import Client
import os
from playsound import playsound
from time import time, sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"
    p = re.compile(regex)
    if (pinCode == ''):
        return False
    m = re.match(p, pinCode)
    if m is None:
        return False
    else:
        return True


def send_mail(email, centers):
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
    message = service.users().messages().send(
        userId='me', body={'raw': raw_string}).execute()



url = "https://selfregistration.cowin.gov.in/"
starttime = time()
centers = []
email = input("Please enter your email :\n")
number = input("Please enter your number")
gecko = input("Enter the path to geckodriver")
driver = webdriver.Firefox(
    executable_path=gecko)
date = datetime.today().strftime('%d-%m-%Y')
i = 0
flag = False
while True:
    i += 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    response = requests.get(
        "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=305&date=%s" % date, headers=headers)
    print(response)
    print("==========RUNNING %s============" % i)
    json_dump = json.dumps(response.json())
    center_data = json.loads(json_dump)
    for center in center_data["centers"]:
        for session in center['sessions']:
            if session['min_age_limit'] == 18:
                if session['available_capacity_dose1'] >= 10:
                    centers.append(center['name'])
                    print(center['name'], center['address'],
                          center['center_id'])
                    playsound('beep.mp3')
                    playsound('beep.mp3')
                    playsound('beep.mp3')
                    playsound('beep.mp3')
                    playsound('beep.mp3')
                    if not (flag):
                        driver.get(url)
                        inputElement = driver.find_element_by_id("mat-input-0")
                        inputElement.send_keys(number)
                        element = WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.sc-ion-loading-md-h.sc-ion-loading-md-s.md.hydrated')))
                        driver.find_element_by_css_selector(".covid-button-desktop.ion-text-center").click()
                        flag = True
sleep(30 - time() % 30)
