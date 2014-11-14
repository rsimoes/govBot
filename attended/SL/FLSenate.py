from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2


def getFLSen(partyDict):
    soup = BeautifulSoup(urllib2.urlopen('http://www.flsenate.gov/Senators/').read())
    table = soup.find('tbody').find_all('tr')
    dictList = []
    for item in table:
        if str(item.get('id')) != 'NoMatch':
            repInfo = {}
            columns = item.find_all('td')
            link = item.find('a', {'class': 'senatorLink'})
            rawName = link.get_text().split(',')
            if len(rawName) == 2:
                repInfo['Name'] = rawName[1].strip() + ' ' + rawName[0].strip()
            elif len(rawName) == 3:
                repInfo['Name'] = rawName[1].strip() + ' ' + rawName[0].strip() + ' ' + rawName[2].strip()
            else:
                repInfo['Name'] = link.get_text().strip()
            repInfo['Website'] = 'http://www.flsenate.gov' + link.get('href')
            repInfo['District'] = 'FL State Senate District {0}'.format(columns[0].get_text().strip())
            repInfo['Party'] = partyDict[str(columns[1].get_text().strip())]
            dictList.append(repInfo)
    return dictList


if __name__ == '__main__':
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getFLSen(partyDict)
    with open(writePath + 'FLSenate.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
