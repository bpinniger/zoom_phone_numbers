from zoom import Zoom
import pprint as pp
import logging

logging.basicConfig(filename="logfile.log", encoding='utf-8', level=logging.DEBUG)

sites = Zoom.listPhoneSites()
Brisbane = next(site for site in sites if site["name"] == "Brisbane")
print (Brisbane["id"])
main = next(site for site in sites if site["name"] == "Main Site")
print (main["id"])

numbers = Zoom.getPhoneNumbers()


brisbaneNumbers = []
mainSiteNumbers = []

for number in numbers:
    phoneNumber = number["number"]
    print (phoneNumber[0:4])
    print (number["site"]["name"])
    if phoneNumber[0:4] == "+617":
        brisbaneNumbers.append(number["id"])
    else:
        mainSiteNumbers.append(number["id"])


pp.pprint(brisbaneNumbers)
if len(brisbaneNumbers) > 0:
    Zoom.updatePhoneNumbers(Brisbane["id"], brisbaneNumbers)

if len(mainSiteNumbers) > 0:
    Zoom.updatePhoneNumbers(main["id"], mainSiteNumbers)