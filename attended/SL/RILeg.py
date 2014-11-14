from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getRILeg(partyDict):
    houseSoup = BeautifulSoup(urllib2.urlopen('http://webserver.rilin.state.ri.us/Email/RepEmailListDistrict.asp', 'lxml').read())
    senateSoup = BeautifulSoup(urllib2.urlopen('http://webserver.rilin.state.ri.us/Email/SenEmailListDistrict.asp', 'lxml').read())
    houseTable = houseSoup.find('tbody').find_all('tr')
    senateTable = senateSoup.find('tbody').find_all('tr')
    dictList = []

    for item in houseTable:
        repInfo = {}
        repInfo['District'] = 'RI State House District ' + item.find('td', {'width': '43'}).string.strip()
        repInfo['Name'] = item.find('td', {'width': '311'}).string.replace('Rep.', '').strip()
        repInfo['Website'] = item.find('td', {'width': '72'}).find('a').get('href')
        repInfo['Email'] = item.find('a', {'href': re.compile('[Mm]ail[Tt]o')}).string.strip()
        repInfo['Phone'] = item.find('td', {'width': '130'}).string.strip()
        dictList.append(repInfo)

    for item in senateTable:
        repInfo = {}
        repInfo['District'] = 'RI State Senate District ' + item.find('td', {'width': '43'}).string.strip()
        repInfo['Name'] = item.find('td', {'width': '311'}).string.replace('Senator', '').strip()
        repInfo['Website'] = item.find('td', {'width': '72'}).find('a').get('href')
        repInfo['Email'] = item.find('a', {'href': re.compile('[Mm]ail[Tt]o')}).string.strip()
        repInfo['Phone'] = item.find('td', {'width': '130'}).string.strip()
        dictList.append(repInfo)

    return dictList


if __name__ == "__main__":
    partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
    dictList = getRILeg(partyDict)
    with open(writePath + 'RILeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
