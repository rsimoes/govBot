from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getIDLeg(partyDict):
    houseSoup = BeautifulSoup(urllib2.urlopen('http://legislature.idaho.gov/house/membership.cfm').read())
    senateSoup = BeautifulSoup(urllib2.urlopen('http://legislature.idaho.gov/senate/membership.cfm').read())
    houseTable = houseSoup.find('table', {'style': 'margin-left: 20px;'}).find_all('tr')
    senateTable = senateSoup.find('table', {'style': 'margin-left: 20px;'}).find_all('tr')
    dictList = []
    emailDict = {}
    counter = 0

    for item in houseTable:
        repInfo = {}
        repInfo['Name'] = item.find('strong').get_text().strip().replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144', 'n').replace(u'\u00f1', 'n').replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['District'] = 'ID State House {0}'.format(re.sub(r'^.*(District [0-9]*).*?$', r'\1', item.get_text()))
        repInfo['Party'] = partyDict[str(re.sub(r'^.*\((.)\).*?$', r'\1', item.get_text()))]
        emailID = re.sub(r'^.*ID=(.*)$', r'\1', item.find('a', {'href': re.compile(r'/about/contactmembersform\.cfm\?ID=')}).get('href'))
        repInfo['Website'] = 'http://legislature.idaho.gov/house/membershipSingle.cfm?ID={0}'.format(emailID)
        if counter == 0:
            emailSoup = BeautifulSoup(urllib2.urlopen('http://legislature.idaho.gov/about/contactmembersform.cfm?ID={0}'.format(emailID)).read())
            emailBlock = str(emailSoup.find('script', {'language': 'JavaScript'})).split(';')
            for i in range(2, len(emailBlock) - 1):
                item = emailBlock[i]
                varList = item.split('=')
                emailDict[varList[0].strip()] = varList[1].strip().replace('"', '').replace("'", '')
        repInfo['Email'] = emailDict['legislators.email{0}'.format(emailID)]
        counter += 1
        dictList.append(repInfo)

    for item in senateTable:
        repInfo = {}
        repInfo['Name'] = item.find('strong').get_text().strip().replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144', 'n').replace(u'\u00f1', 'n').replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['District'] = 'ID State Senate {0}'.format(re.sub(r'^.*(District [0-9]*).*?$', r'\1', item.get_text()))
        repInfo['Party'] = partyDict[str(re.sub(r'^.*\((.)\).*?$', r'\1', item.get_text()))]
        emailID = re.sub(r'^.*ID=(.*)$', r'\1', item.find('a', {'href': re.compile(r'/about/contactmembersform\.cfm\?ID=')}).get('href'))
        repInfo['Website'] = 'http://legislature.idaho.gov/house/membershipSingle.cfm?ID={0}'.format(emailID)
        if counter == 0:
            emailSoup = BeautifulSoup(urllib2.urlopen('http://legislature.idaho.gov/about/contactmembersform.cfm?ID={0}'.format(emailID)).read())
            emailBlock = emailSoup.find('script', {'language': 'JavaScript'}).split(';')
        repInfo['Email'] = emailDict['legislators.email{0}'.format(emailID)]
        dictList.append(repInfo)

    return dictList


if __name__ == '__main__':
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getIDLeg(partyDict)
    with open(writePath + 'IDLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
