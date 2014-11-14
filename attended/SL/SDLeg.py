from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getSDLeg(partyDict):
    houseSoup = BeautifulSoup(urllib2.urlopen('http://legis.sd.gov/Legislators/Legislators/Roster.aspx?Body=H').read())
    senateSoup = BeautifulSoup(urllib2.urlopen('http://legis.sd.gov/Legislators/Legislators/Roster.aspx?Body=S').read())
    houseTable = houseSoup.find('table', {'class': 'roster'}).find_all('tr')
    senateTable = senateSoup.find('table', {'class': 'roster'}).find_all('tr')
    dictList = []

    for item in houseTable:
        repInfo = {}
        columns = item.find_all('td')
        if len(columns) > 0:
            link = columns[0].find('a')
            nameList = link.string.split(',')
            if len(nameList) == 2:
                repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
            elif len(nameList) == 3:
                repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
            else:
                repInfo['Name'] = link.get_text().strip()
            repInfo['Name'] = repInfo['Name'].replace('   ', ' ').replace('  ', ' ')
            repInfo['Website'] = 'http://legis.sd.gov/Legislators/Legislators/' + link.get('href')
            repInfo['Party'] = partyDict[str(columns[2].get_text().strip())]
            repInfo['District'] = 'SD State House District {0}'.format(re.sub('^0', '', columns[1].get_text().strip()))
            repInfo['Address'] = '{0} {1}, SD {2}'.format(columns[3].get_text().strip(), columns[4].get_text().strip(), columns[5].get_text().strip(), )
            dictList.append(repInfo)

    for item in senateTable:
        repInfo = {}
        columns = item.find_all('td')
        if len(columns) > 0:
            link = columns[0].find('a')
            nameList = link.string.split(',')
            if len(nameList) == 2:
                repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
            elif len(nameList) == 3:
                repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
            else:
                repInfo['Name'] = link.get_text().strip()
            repInfo['Name'] = repInfo['Name'].replace('   ', ' ').replace('  ', ' ')
            repInfo['Website'] = 'http://legis.sd.gov/Legislators/Legislators/' + link.get('href')
            repInfo['Party'] = partyDict[str(columns[2].get_text().strip())]
            repInfo['District'] = 'SD State Senate District {0}'.format(re.sub('^0', '', columns[1].get_text().strip()))
            repInfo['Address'] = '{0} {1}, SD {2}'.format(columns[3].get_text().strip(), columns[4].get_text().strip(), columns[5].get_text().strip(), )
            dictList.append(repInfo)

    return dictList


if __name__ == "__main__":
    partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
    dictList = getSDLeg(partyDict)
    with open(writePath + 'SDLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
