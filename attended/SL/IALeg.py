import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getIALeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('https://www.legis.iowa.gov/legislators/house').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('https://www.legis.iowa.gov/legislators/senate').read())

  table = houseSoup.find('table', {'id': 'sortableTable'}).find('tbody').find_all('tr') + senateSoup.find('table', {'id': 'sortableTable'}).find('tbody').find_all('tr')

  dictList = []

  for item in table:
    repInfo = {}

    columns = item.find_all('td')
    link = columns[1].find('a')
    repInfo['District'] = 'IA State {0} District {1}'.format(columns[0].get_text().strip(), columns[2].get_text().strip())
    repInfo['Website'] = 'https://www.legis.iowa.gov' + link.get('href')
    repInfo['Name'] = link.get_text().strip()
    repInfo['Party'] = partyDict[str(columns[3].get_text().strip())]
    repInfo['Email'] = columns[5].get_text().strip()

    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getIALeg(partyDict)

  with open('/home/michael/Desktop/IALeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)