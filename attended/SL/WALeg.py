from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2


def getWALeg(partyDict):
    soup = BeautifulSoup(urllib2.urlopen('http://apps.leg.wa.gov/rosters/Members.aspx').read(), 'lxml')
    table = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_dgMembers'}).find_all('tr')
    chamberDict = {'S': 'Senate', 'H': 'House'}
    dictList = []
    for i in range(1, len(table)):
        repInfo = {}
        columns = table[i].find_all('td')
        link = columns[0].find('a')
        name = ''
        nameList = link.get_text().split(', ')
        if len(nameList) == 2:
            name = nameList[1].strip() + ' ' + nameList[0].strip()
        elif len(nameList) == 3:
            name = nameList[1].strip() + ' ' + nameList[2].strip() + ' ' + nameList[0].strip()
        else:
            name = table[i].find('b').get_text().strip()
        repInfo['Name'] = name.strip().replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144', 'n').replace(u'\u00f1', 'n').replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['Website'] = link.get('href')
        repInfo['Party'] = partyDict[str(columns[1].get_text().strip())]
        repInfo['District'] = 'WA State {0} District {1}'.format(chamberDict[str(columns[6].get_text().strip())], columns[2].get_text().strip())
        repInfo['Phone'] = columns[5].get_text().strip()
        dictList.append(repInfo)
    return dictList


if __name__ == "__main__":
    partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
    dictList = getWALeg(partyDict)
    with open(writePath + 'WALeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
