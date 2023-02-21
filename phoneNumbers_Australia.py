from zoom import Zoom
import pprint as pp
import logging

logging.basicConfig(filename="logfile.log", encoding='utf-8', level=logging.DEBUG)

#get site details - we will need the site Id to update the phone numbers
sites = Zoom.listPhoneSites()
Brisbane = next(site for site in sites if site["name"] == "Brisbane")
main = next(site for site in sites if site["name"] == "Main Site")

#get unassigned phone numbers
numbers = Zoom.getPhoneNumbers()
brisbaneNumbers = []
mainSiteNumbers = []

for number in numbers:
    phoneNumber = number["number"]
    if phoneNumber[0:4] == "+617":
        brisbaneNumbers.append(number["id"])
    else:
        mainSiteNumbers.append(number["id"])

#update phone numbers for each site Id
if len(brisbaneNumbers) > 0:
    Zoom.updatePhoneNumbers(Brisbane["id"], brisbaneNumbers)

if len(mainSiteNumbers) > 0:
    Zoom.updatePhoneNumbers(main["id"], mainSiteNumbers)