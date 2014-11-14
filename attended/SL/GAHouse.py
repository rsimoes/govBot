from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getGAHouse(partyDict):
    soup = BeautifulSoup(urllib2.urlopen('http://www.house.ga.gov/Representatives/en-US/HouseMembersList.aspx').read())
    table = soup.find('div', {'style': 'font-size:13px;'}).find_all('span')
    dictList = []
    for i in range(len(table) / 3):
        repInfo = {}
        repInfo
        nameInfo = table[i * 3].find('a')
        relativeWebsite = nameInfo.get('href')
        nameList = nameInfo.string.replace(")", "").replace("(", ", ").split(",")
        repInfo['District'] = 'GA State House District ' + table[i * 3 + 1].string.strip()
        repInfo['Party'] = partyDict[str(nameList[len(nameList) - 1].strip())]
        nameList.remove(nameList[len(nameList) - 1])
        if len(nameList) == 2:
            repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
        elif len(nameList) == 3:
            repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
        else:
            repInfo['Name'] = ''
            for item in nameList:
                repInfo['Name'] = repInfo['Name'] + ' ' + item.strip()
            repInfo['Name'].strip()
        repInfo['Website'] = 'http://www.house.ga.gov/Representatives/en-US' + re.sub("^\\.", "", relativeWebsite)
        dictList.append(repInfo)
    return dictList


if __name__ == '__main__':
    partyDict = {'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getGAHouse(partyDict)
    with open(writePath + 'GAHouse.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Website', 'Party'])
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
