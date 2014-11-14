from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getINLeg(partyDict):
    starterSoup = BeautifulSoup(urllib2.urlopen('http://iga.in.gov/').read())
    url = starterSoup.find('a', {'href': re.compile('legislative/[0-9]*/legislators')}).get('href')
    soup = BeautifulSoup(urllib2.urlopen('http://iga.in.gov' + url).read())
    dictList = []
    senators = soup.find('optgroup', {'id': 'Senators'}).find_all('option')
    reps = soup.find('optgroup', {'id': 'Representatives'}).find_all('option')

    for senator in senators:
        senInfo = {}
        splitInfo = senator.string.strip().split(',')
        if len(splitInfo) == 3:
            rawName = splitInfo[0].strip()
        else:
            rawName = splitInfo[0].strip() + ' ' + splitInfo[1].strip()
        senInfo['District'] = 'IN State Senate ' + splitInfo[len(splitInfo) - 1].strip()
        senInfo['Name'] = rawName[5:].strip()
        senInfo['Party'] = splitInfo[len(splitInfo) - 2].strip()
        senInfo['Website'] = 'http://iga.in.gov' + senator.get('value')
        dictList.append(senInfo)

    for rep in reps:
        repInfo = {}
        splitInfo = rep.string.strip().split(',')
        if len(splitInfo) == 3:
            rawName = splitInfo[0].strip()
        else:
            rawName = splitInfo[0].strip() + ' ' + splitInfo[1].strip()
        repInfo['District'] = 'IN State House ' + splitInfo[len(splitInfo) - 1].strip()
        repInfo['Name'] = rawName[5:].strip()
        repInfo['Party'] = splitInfo[len(splitInfo) - 2].strip()
        repInfo['Website'] = 'http://iga.in.gov' + rep.get('value')
        dictList.append(repInfo)

    return dictList


if __name__ == '__main__':
    dictList = getINLeg("")
    with open(writePath + 'INLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website'])
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
