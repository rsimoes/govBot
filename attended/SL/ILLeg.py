from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2


def getILLeg(partyDict):
    houseSoup = BeautifulSoup(urllib2.urlopen('http://www.ilga.gov/house/').read(), 'lxml')
    senateSoup = BeautifulSoup(urllib2.urlopen('http://www.ilga.gov/senate/').read(), 'lxml')
    houseTable = houseSoup.find('table', {'cellpadding': '3'}).find_all('tr')
    senateTable = senateSoup.find('table', {'cellpadding': '3'}).find_all('tr')
    dictList = []

    for i in range(2, len(houseTable)):
        columns = houseTable[i].find_all('td')
        repInfo = {}
        link = columns[0].find('a')
        repInfo['Name'] = link.get_text().strip().replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144', 'n').replace(u'\u00f1', 'n').replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['Website'] = 'http://www.ilga.gov' + link.get('href')
        repInfo['District'] = 'IL State House District {0}'.format(columns[3].get_text().strip())
        repInfo['Party'] = partyDict[str(columns[4].get_text().strip())]
        dictList.append(repInfo)

    for i in range(2, len(senateTable)):
        columns = senateTable[i].find_all('td')
        repInfo = {}
        link = columns[0].find('a')
        repInfo['Name'] = link.get_text().strip().replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144', 'n').replace(u'\u00f1', 'n').replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['Website'] = 'http://www.ilga.gov' + link.get('href')
        repInfo['District'] = 'IL State Senate District {0}'.format(columns[3].get_text().strip())
        repInfo['Party'] = partyDict[str(columns[4].get_text().strip())]
        dictList.append(repInfo)

    return dictList


if __name__ == '__main__':
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getILLeg(partyDict)
    with open(writePath + 'ILLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
