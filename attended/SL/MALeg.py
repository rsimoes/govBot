from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2


def getDistrict(url, branch):
    ordinalDict = {'first': '1', 'second': '2', 'third': '3', 'fourth': '4', 'fifth': '5', 'sixth': '6', 'seventh': '7', 'eighth': '8', 'ninth': '9', 'tenth': '10', 'eleventh': '11', 'twelfth': '12', 'thirteenth': '13', 'fourteenth': '14', 'fifteenth': '15', 'sixteenth': '16', 'seventeenth': '17', 'eighteenth': '18', 'nineteenth': '19', 'twentieth': '20', 'thirtieth': '30', 'fortieth': '40', 'fiftieth': '50', 'sixtieth': '60', 'seventieth': '70', 'eightieth': '80', 'ninetieth': '9', 'twenty': '2', 'thirty': '3', 'forty': '4', 'fifty': '5', 'sixty': '6', 'seventy': '7', 'eighty': '8', 'ninety': '9'}
    while True:
        try:
            print url
            response = urllib2.urlopen(url, timeout=10)
            soup = BeautifulSoup(response.read(), 'html5lib')
            distList = soup.find('div', {'id': 'District'}).get_text().replace(' - ', ' -- ').replace(".", "--").replace('consistng', '--').replace('consiting', '--').replace('consisting', '--').replace('Consisting', '--').split('--')[0].strip().replace(', ', ' ').replace('     ', ' ').replace('    ', ' ').split(' ')
            ordinalList = distList[0].split('-')
            lastString = ordinalList[len(ordinalList) - 1]
            distNum = ''
            if ordinalList[0].lower() in ordinalDict.keys():
                for i in range(len(ordinalList)):
                    distNum = distNum + ordinalDict[ordinalList[i].lower()]
                distNum = distNum + lastString[len(lastString) - 2:]
                townName = ''
                for i in range(1, len(distList)):
                    townName = townName + ' ' + distList[i]
                townName = townName.strip()
                district = 'MA State {0} District {1} {2}'.format(branch, distNum, townName)
            else:
                townName = ''
                for i in range(len(distList)):
                    townName = townName + ' ' + distList[i]
                townName = townName.strip()
                district = 'MA State {0} District {1}'.format(branch, townName)
            return district
        except Exception:
            pass


def getMAHouse(partyDict):
    ##The MA Website lacks a standard district listing, this will catch most (but not all) district names
    houseSoup = BeautifulSoup(urllib2.urlopen('https://malegislature.gov/People/House').read())
    table = houseSoup.find_all('tr', {'class': 'dataRow'})
    dictList = []
    for rep in table:
        repInfo = {}
        links = rep.find_all('a')
        nameLink = links[0]
        emailLink = links[2]
        repInfo['Name'] = nameLink.get('title').strip().replace("     ", " ").replace("    ", " ").replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['Party'] = partyDict[rep.find('td', {'class': 'partyCol'}).string.strip()]
        repInfo['Website'] = 'https://malegislature.gov' + nameLink.get('href')
        repInfo['Email'] = emailLink.string.strip()
        repInfo['Phone'] = rep.find('td', {'class': lambda x: x and x.lower() == 'phonecol'}).string.strip()
        repInfo['Address'] = 'State House Room {0} Boston, MA 02133'.format(rep.find('td', {'class': 'locationCol'}).string.strip())
        repInfo['District'] = getDistrict(repInfo['Website'], 'House')
        dictList.append(repInfo)
    return dictList


def getMASenate(partyDict):
    ##The MA Website lacks a standard district listing, this will catch most (but not all) district names
    senateSoup = BeautifulSoup(urllib2.urlopen('https://malegislature.gov/People/Senate').read())
    table = senateSoup.find_all('tr', {'class': 'dataRow'})
    dictList = []
    for rep in table:
        repInfo = {}
        links = rep.find_all('a')
        nameLink = links[0]
        emailLink = links[2]
        repInfo['Name'] = nameLink.get('title').strip().replace("     ", " ").replace("    ", " ").replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['Party'] = partyDict[rep.find('td', {'class': 'partyCol'}).string.strip()]
        repInfo['Website'] = 'https://malegislature.gov' + nameLink.get('href')
        repInfo['Email'] = emailLink.string.strip()
        repInfo['Phone'] = rep.find('td', {'class': lambda x: x and x.lower() == 'phonecol'}).string.strip()
        repInfo['Address'] = 'State House Room {0} Boston, MA 02133'.format(rep.find('td', {'class': 'locationCol'}).string.strip())
        repInfo['District'] = getDistrict(repInfo['Website'], 'Senate')
        dictList.append(repInfo)
    return dictList


if __name__ == '__main__':
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getMAHouse(partyDict) + getMASenate(partyDict)
    with open(writePath + 'MALeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
