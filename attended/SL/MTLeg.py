from csv import DictWriter, DictReader
from bs4 import BeautifulSoup
from StringIO import StringIO
from config import writePath
import urllib2
import re


def getMTLeg(partyDict):
    starterSoup = BeautifulSoup(urllib2.urlopen('http://leg.mt.gov/css/find%20a%20legislator.asp').read())
    infoURL = starterSoup.find('a', {'href': re.compile(r'roster\.asp')}).get('href')
    secondSoup = BeautifulSoup(urllib2.urlopen('http://leg.mt.gov/css/' + infoURL).read())
    url = secondSoup.find('a', {'href': re.compile(r'FullMembers\.txt')}).get('href')
    text = urllib2.urlopen('http://leg.mt.gov' + url).read()
    input = StringIO(text)
    drObject = DictReader(input)
    dictList = []
    for item in drObject:
        repInfo = {}
        chambers = {'HD': 'House', 'SD': 'Senate'}
        distInfo = item['Districts'].split(' ')
        repInfo['Name'] = '{0} {1}'.format(item['FirstName'], item['LastName']).title().strip()
        repInfo['District'] = 'MT State {0} District {1}'.format(chambers[distInfo[0]], distInfo[1])
        repInfo['Party'] = partyDict[str(item['PartyAbbrev'])]
        repInfo['Address'] = '{0} {1}, {2} {3}'.format(item['Addr_Ln_1'], item['City'], item['StateProvince'], item['PostalCode'])
        dictList.append(repInfo)
    return dictList


if __name__ == "__main__":
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getMTLeg(partyDict)
    with open(writePath + 'MTLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
