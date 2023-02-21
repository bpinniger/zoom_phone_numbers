import requests
import logging
import os
from dotenv import load_dotenv
import json
from requests.api import head
import base64

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

S2S_ClientID = os.environ.get('S2S_ClientID')
S2S_ClientSecret = os.environ.get('S2S_ClientSecret')
S2S_AcctID = os.environ.get('S2S_AcctID')

baseURL = "https://api.zoom.us/v2/"

def getS2S_Token():
    url = "https://zoom.us/oauth/token?grant_type=account_credentials&account_id=" + S2S_AcctID
    S2SCreds = S2S_ClientID + ":" + S2S_ClientSecret
    S2SCreds_bytes = S2SCreds.encode("ascii")
    S2SCreds_b64 = base64.b64encode(S2SCreds_bytes)
    b64string = S2SCreds_b64.decode("ascii")
    payload={}
    headers = {
    'Authorization': 'Basic  ' + b64string
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        results = json.loads(response.text)
        token = results["access_token"]
        return token
    else:
        logging.error("failed to get S2S Access Token")
        logging.error(response.text)
        return ""

S2Stoken = getS2S_Token()

class Zoom:

    def listPhoneSites():
        url = "%s/phone/sites?page_size=30" % (baseURL)
        payload={}
        headers = {
        'Authorization': 'Bearer '+ S2Stoken
        }
        sites = []
        response = requests.request("GET", url, headers=headers, data=payload)
        results = json.loads(response.text)
        if response.status_code == 200:
            try:
                sites = results["sites"]
            except Exception as e:
                logging.warning ("no sites exist")
                logging.warning (e)
        else:
            logging.error("failed to get sites")
            logging.error(response.text)
        return sites

    def getPhoneNumbers():
        url = "%s/phone/numbers?type=unassigned&page_size=100" % (baseURL)
        headers = {
        'Authorization': 'Bearer ' + S2Stoken
        }
        response = requests.request("GET", url, headers=headers, data="")
        results = json.loads(response.text)
        if response.status_code == 200:
            return results["phone_numbers"]
        else:
            logging.error("failed to get phone numbers")
            logging.error(response.text)
            return {}

    def updatePhoneNumbers(siteId, phonenumbers):
        url = "%s/phone/numbers/sites/%s" % (baseURL, siteId)
        payload = json.dumps({
            "phone_numbers": phonenumbers
            })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + S2Stoken
        }
        response = requests.patch(url, headers=headers, data=payload)
        if response.status_code == 204:
            logging.info("phone numbers updated")
        else:
            logging.error("failed to update phone numbers")
            logging.error(response.text)
