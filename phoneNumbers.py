from zoom import Zoom
import pprint as pp
import logging

logging.basicConfig(filename="logfile.log", encoding='utf-8', level=logging.DEBUG)

#get site details - we will need the site Id to update the phone numbers
sites = Zoom.listPhoneSites()
West = next(site for site in sites if site["name"] == "West")
Central = next(site for site in sites if site["name"] == "Central")
main = next(site for site in sites if site["name"] == "Main Site")

#get unassigned phone numbers
numbers = Zoom.getPhoneNumbers()
westNumbers = []
centralNumbers = []
mainSiteNumbers = []
for number in numbers:
    phoneNumber = number["number"]
    if phoneNumber[1:4] == "828":
        westNumbers.append(number["id"])
    elif phoneNumber[1:4] == "252":
        mainSiteNumbers.append(number["id"])
    else:
        centralNumbers.append(number["id"])


#update phone numbers for each site Id
if len(westNumbers) > 0:
    Zoom.updatePhoneNumbers(West["id"], westNumbers)

if len(centralNumbers) > 0:
    Zoom.updatePhoneNumbers(Central["id"], centralNumbers)

if len(mainSiteNumbers) > 0:
    Zoom.updatePhoneNumbers(main["id"], mainSiteNumbers)