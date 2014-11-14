from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getORLeg(partyDict):
    houseSoup = BeautifulSoup(urllib2.urlopen('https://www.oregonlegislature.gov/house/Pages/RepresentativesAll.aspx').read().decode('utf-8').replace(u'\u200b', ' ').replace(u'\xe2', "'").replace('\n', ' '), 'html5lib')
    senateSoup = BeautifulSoup(urllib2.urlopen('https://www.oregonlegislature.gov/senate/Pages/SenatorsAll.aspx').read().decode('utf-8').replace(u'\u200b', ' ').replace(u'\xe2', "'").replace('\n', ' '), 'html5lib')
    houseTable = houseSoup.find('table', {'class': 'ms-listviewtable'}).find_all('tr')
    senateTable = senateSoup.find('table', {'class': 'ms-listviewtable'}).find_all('tr')
    dictList = []

    for i in range(1, len(houseTable)):
        item = houseTable[i]
        repInfo = {}
        links = item.find_all('a')
        paragraphs = item.find_all('p')
        partyDist = paragraphs[0].get_text().strip().replace(u'\u00a0', ' ').replace('\r', ' ').replace(u'\u20ac', ' ').replace(u'\u2039', ' ').replace("'", ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
        relativeLocation = links[0].get('href')
        rawDist = re.sub(re.compile(r'^.*District: .*?([0-9]*).*$', re.DOTALL), r'\1', partyDist)
        repInfo['District'] = 'OR State House District {0}'.format(rawDist)
        if str(relativeLocation) != 'http://www.oregonlegislature.gov/':
            if str(links[0].get('href')[:4]) == 'http':
                repInfo['Party'] = partyDict[str(re.sub(r'^.*Party: ([RD][a-z]*).*?$', r'\1', partyDist))]
                repInfo['Name'] = links[0].get_text().replace('Representative', '').replace(u'\u20ac', '').replace(u'\u2039', '').replace("'", '').replace(u'\u00a0', ' ').strip()
                repInfo['Website'] = links[0].get('href')
            else:
                repInfo['Party'] = partyDict[str(re.sub(r'^.*Party: ([RD][a-z]*).*?$', r'\1', partyDist.replace('\n', ' ')))]
                repInfo['Name'] = links[0].get_text().replace('Representative', '').replace(u'\u20ac', '').replace(u'\u2039', '').replace("'", '').replace(u'\u00a0', ' ').strip()
                repInfo['Website'] = 'https://www.oregonlegislature.gov' + links[0].get('href')
        else:
            repInfo['Name'] = 'VACANT'
            repInfo['Website'] = relativeLocation
        if len(links) > 1:
            repInfo['Email'] = item.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]:')}).get_text()
        dictList.append(repInfo)

    for i in range(1, len(senateTable)):
        item = senateTable[i]
        repInfo = {}
        links = item.find_all('a')
        paragraphs = item.find_all('p')
        partyDist = paragraphs[0].get_text().strip().replace(u'\u00a0', ' ').replace('\r', ' ').replace(u'\u20ac', '').replace(u'\u2039', '').replace("'", '')
        relativeLocation = links[0].get('href')
        rawDist = re.sub(re.compile(r'^.*District: .*?([0-9]*).*$', re.DOTALL), r'\1', partyDist)
        repInfo['District'] = 'OR State Senate District {0}'.format(rawDist)
        if str(relativeLocation) != 'http://www.oregonlegislature.gov/':
            if str(links[0].get('href')[:4]) == 'http':
                repInfo['Party'] = partyDict[str(re.sub(r'^.*Party: ([RD][a-z]*).*?$', r'\1', partyDist))]
                repInfo['Name'] = links[0].get_text().replace('Senator', '').replace(u'\u20ac', '').replace(u'\u2039', '').replace("'", '').replace(u'\u00a0', ' ').strip()
                repInfo['Website'] = links[0].get('href')
            else:
                repInfo['Party'] = partyDict[str(re.sub(r'^.*Party: ([RD][a-z]*).*?$', r'\1', partyDist))]
                repInfo['Name'] = links[0].get_text().replace('Senator', '').replace(u'\u20ac', '').replace(u'\u2039', '').replace("'", '').replace(u'\u00a0', ' ').strip()
                repInfo['Website'] = 'https://www.oregonlegislature.gov' + links[0].get('href')
        else:
            repInfo['Name'] = 'VACANT'
            repInfo['Website'] = relativeLocation
        if len(links) > 1:
            repInfo['Email'] = item.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]:')}).get_text()
        dictList.append(repInfo)

    return dictList


if __name__ == "__main__":
    partyDict = {'Dem': 'Democratic', 'Rep': 'Republican', '(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getORLeg(partyDict)
    with open(writePath + 'ORLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
