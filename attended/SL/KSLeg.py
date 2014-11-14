from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getKSRep(url, partyDict):
    while True:
        try:
            print url
            response = urllib2.urlopen(url, timeout=10)
            soup = BeautifulSoup(response.read(), 'lxml')
            main = soup.find('div', {'id': 'main'})
            name = re.sub('(Representative)|(Senator)', '', main.find('h1').get_text()).split(' - ')[0].strip().replace('    ', ' ')
            party = partyDict[str(re.sub(r'^.*Party:\s([A-Za-z]*)\s.*$', r'\1', main.find('h3').get_text()))]
            return name, party
        except Exception:
            pass


def getKSLeg(partyDict):
    starterSoup = BeautifulSoup(urllib2.urlopen('http://www.kslegislature.org', 'lxml').read())
    houseURL = starterSoup.find('a', {'href': re.compile('house/roster')}).get('href')
    senateURL = starterSoup.find('a', {'href': re.compile('senate/roster')}).get('href')
    houseSoup = BeautifulSoup(urllib2.urlopen('http://www.kslegislature.org' + houseURL, 'lxml').read())
    senateSoup = BeautifulSoup(urllib2.urlopen('http://www.kslegislature.org' + senateURL, 'lxml').read())
    houseTable = houseSoup.find('table', {'class': 'bottom'}).find_all('tr')
    senateTable = senateSoup.find('table', {'class': 'bottom'}).find_all('tr')
    dictList = []

    for i in range(1, len(houseTable)):
        repInfo = {}
        columns = houseTable[i].find_all('td')
        repInfo['District'] = 'KS State House District {0}'.format(columns[1].get_text().strip())
        repInfo['Website'] = 'http://www.kslegislature.org' + columns[0].find('a').get('href')
        repInfo['Email'] = columns[3].get_text().strip()
        repInfo['Phone'] = columns[2].get_text().strip()
        repInfo['Name'], repInfo['Party'] = getKSRep(repInfo['Website'], partyDict)
        dictList.append(repInfo)

    for i in range(1, len(senateTable)):
        repInfo = {}
        columns = senateTable[i].find_all('td')
        repInfo['District'] = 'KS State Senate District {0}'.format(columns[1].get_text().strip())
        repInfo['Website'] = 'http://www.kslegislature.org' + columns[0].find('a').get('href')
        repInfo['Email'] = columns[3].get_text().strip()
        repInfo['Phone'] = columns[2].get_text().strip()
        repInfo['Name'], repInfo['Party'] = getKSRep(repInfo['Website'], partyDict)
        dictList.append(repInfo)

    return dictList


if __name__ == "__main__":
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getKSLeg(partyDict)
    with open(writePath + 'KSLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
