from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2


def getFLHouse(partyDict):
    soup = BeautifulSoup(urllib2.urlopen('http://www.myfloridahouse.gov/Sections/Representatives/representatives.aspx?SortField=district&SortDirection=asc&LastSortField=Name').read())
    rawReps = soup.find_all('div', {'class': 'rep_style'})
    rawDistricts = soup.find_all('div', {'class': 'district_style'})
    rawParties = soup.find_all('div', {'class': 'party_style'})
    rawTerms = soup.find_all('div', {'class': 'term_style'})
    dictList = []
    if len(rawReps) == len(rawDistricts) == len(rawParties) == len(rawTerms):
        for i in range(len(rawReps)):
            repDict = {}
            rep = rawReps[i]
            district = rawDistricts[i].string.replace(" ", "").strip()
            party = rawParties[i].string.replace(" ", "").strip()
            website = 'http://www.myfloridahouse.gov' + rep.find('a').get('href')
            nameList = rep.find('a').string.split(', ')
            if len(nameList) == 2:
                name = nameList[1].strip() + ' ' + nameList[0].strip()
            elif len(nameList) > 2:
                name = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
            else:
                name = rep.find('a').string.strip()
            name = name.replace(u'\u2018', "'").replace(u'\u0144', 'n').replace(u'\u00f1', 'n').replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u').encode('utf-8', 'replace').replace('     ', ' ').replace('    ', ' ')
            repDict['Name'] = name
            repDict['District'] = 'FL State House District ' + district
            repDict['Party'] = partyDict[party]
            repDict['Website'] = website
            dictList.append(repDict)
    return dictList


if __name__ == '__main__':
    partyDict = {'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent'}
    dictList = getFLHouse(partyDict)
    with open(writePath + 'FLHouse.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website'])
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
