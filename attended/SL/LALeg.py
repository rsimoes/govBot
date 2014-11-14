from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getLALeg(partyDict):
    houseSoup = BeautifulSoup(urllib2.urlopen('http://house.louisiana.gov/H_Reps/H_Reps_FullInfo.asp').read(), 'lxml')
    housePartySoup = BeautifulSoup(urllib2.urlopen('http://house.louisiana.gov/H_Reps/H_Reps_ByParty.asp').read(), 'lxml')
    senateSoup = BeautifulSoup(urllib2.urlopen('http://senate.la.gov/senators/ByDistrict.asp').read(), 'lxml')
    houseTable = houseSoup.find('tbody').find_all('tr')
    housePartyTable = housePartySoup.find('tbody').find_all('tr')
    senateTable = senateSoup.find('table', {'cellpadding': '4'}).find_all('tr')
    repParties = {}
    dictList = []

    for item in housePartyTable:
        columns = item.find_all('td')
        repParties[columns[0].get_text().strip()] = partyDict[str(columns[1].get_text().strip())]

    for item in houseTable:
        repInfo = {}
        columns = item.find_all('td')
        link = columns[0].find('a')
        name = ''
        rawName = link.get_text().strip()
        nameList = rawName.split(', ')
        if len(nameList) == 2:
            name = nameList[1].strip() + ' ' + nameList[0].strip()
        elif len(nameList) == 3:
            name = nameList[2].strip() + ' ' + nameList[1].strip() + ' ' + nameList[0].strip()
        else:
            name = rawName
        repInfo['Name'] = name.replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144', 'n').replace(u'\u00f1', 'n').replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['Party'] = repParties[rawName]
        repInfo['District'] = 'LA State House District {0}'.format(columns[1].get_text().strip())
        repInfo['Website'] = 'http://house.louisiana.gov/' + link.get('href').replace('..', '')
        repInfo['Address'] = columns[2].get_text().replace('\n', ' ').replace('\r', ' ').replace('   ', ' ').replace('  ', ' ').strip()
        repInfo['Phone'] = columns[3].get_text().strip()
        repInfo['Email'] = columns[4].get_text().strip()
        dictList.append(repInfo)

    for i in range(1, len(senateTable)):
        repInfo = {}
        columns = senateTable[i].find_all('td')
        link = columns[3].find('a')
        repInfo['District'] = 'LA State Senate District {0}'.format(columns[0].get_text().replace('#', '').strip())
        repInfo['Name'] = link.get_text().replace('Senator', '').strip().replace(u'\u00A0', ' ').replace('     ', ' ').replace('    ', ' ').replace(u'\u0144', 'n').replace(u'\u00f1', 'n').replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['Website'] = 'http://senate.la.gov' + link.get('href')
        repInfo['Email'] = re.sub(r'^.*[Mm][Aa][Ii][Ll][Tt][Oo]:(.*)$', r'\1', columns[1].find('a').get('href'))
        dictList.append(repInfo)

    return dictList


if __name__ == "__main__":
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getLALeg(partyDict)
    with open(writePath + 'LALeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
