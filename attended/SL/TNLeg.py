from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getTNLeg(partyDict):
    houseSoup = BeautifulSoup(urllib2.urlopen('http://www.capitol.tn.gov/house/members/').read())
    senateSoup = BeautifulSoup(urllib2.urlopen('http://www.capitol.tn.gov/senate/members/').read())
    houseTable = houseSoup.find('tbody').find('tbody').find_all('tr')
    senateTable = senateSoup.find('tbody').find_all('tr')
    dictList = []

    for item in houseTable:
        repInfo = {}
        columns = item.find_all('td')
        link = columns[0].find('a')
        nameList = columns[0].get_text().split(',')
        addressList = columns[4].get_text().replace('WMB', ' WMB').replace('LP', ' LP').replace('    ', ' ').strip().split(' ')
        if len(addressList) < 2:
            addressList = ['', '']
        if len(nameList) == 2:
            repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
        elif len(nameList) == 3:
            repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
        else:
            repInfo['Name'] = link.get_text().strip()
        repInfo['Name'] = repInfo['Name'].replace('   ', ' ').replace('  ', ' ').replace('Speaker ', '')
        repInfo['Website'] = 'http://www.capitol.tn.gov/house/members/' + link.get('href')
        repInfo['Party'] = partyDict[str(columns[1].get_text().strip())]
        repInfo['District'] = 'TN State House {0}'.format(columns[3].get_text().strip())
        repInfo['Address'] = '301 6th Avenue North Suite {0}, {1} Nashville, TN 37243'.format(addressList[0], addressList[1])
        repInfo['Phone'] = '(615) {0}'.format(columns[5].get_text().strip())
        repInfo['Email'] = columns[6].get_text().strip()
        dictList.append(repInfo)

    for item in senateTable:
        if len(addressList) < 2:
            addressList = ['', '']
        repInfo = {}
        columns = item.find_all('td')
        link = columns[0].find('a')
        nameList = columns[0].get_text().split(',')
        addressList = columns[4].get_text().replace('WMB', ' WMB').replace('LP', ' LP').replace('  ', ' ').strip().split(' ')
        if len(nameList) == 2:
            repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
        elif len(nameList) == 3:
            repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
        else:
            repInfo['Name'] = link.get_text().strip()
        repInfo['Name'] = repInfo['Name'].replace('   ', ' ').replace('  ', ' ').replace('Lt. Gov.', '').strip()
        if re.search('^http:', link.get('href')):
            repInfo['Website'] = link.get('href')
        else:
            repInfo['Website'] = 'http://www.capitol.tn.gov/senate/members/' + link.get('href')
        repInfo['Party'] = partyDict[str(columns[1].get_text().strip())]
        repInfo['District'] = 'TN State Senate {0}'.format(columns[3].get_text().strip())
        repInfo['Address'] = '301 6th Avenue North Suite {0}, {1} Nashville, TN 37243'.format(addressList[0], addressList[1])
        repInfo['Phone'] = '(615) {0}'.format(columns[5].get_text().strip())
        repInfo['Email'] = columns[6].get_text().strip()
        dictList.append(repInfo)

    return dictList


if __name__ == "__main__":
    partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
    dictList = getTNLeg(partyDict)
    with open(writePath + 'TNLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
