import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getAZrep(url):
  print url
  email = ''
  response = urllib2.urlopen(url)

  if response.code == 200:
    soup = BeautifulSoup(response.read())

    tempEmail = soup.find('a', {'href': re.compile('mailto')})
    if tempEmail is not None:
      email = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', tempEmail.get('href'))

  return email


def getAZLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.azleg.gov/MemberRoster.asp?Body=H').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.azleg.gov/MemberRoster.asp?Body=S').read())

  houseTable = houseSoup.find('table', {'id': 'house'}).find_all('tr')
  senateTable = senateSoup.find('table', {'id': 'senate'}).find_all('tr')

  dictList = []

  for i in range(1, len(houseTable)):
    item = houseTable[i]
    repInfo = {}

    columns = item.find_all('td')
    link = columns[0].find('a')

    repInfo['Name'] = link.get_text().strip().replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Website'] = 'http://www.azleg.gov' + link.get('href')
    repInfo['District'] = 'AL State House District {0}'.format(columns[1].get_text().strip())
    repInfo['Party'] = partyDict[str(columns[2].get_text().strip())]
    repInfo['Email'] = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', columns[3].find('a').get('href'))
    repInfo['Address'] = '1700 West Washington, Room {0}, Phoenix, AZ 85007-2890'.format(columns[4].get_text().strip())
    repInfo['Phone'] = '(602)-{0}'.format(columns[5].get_text().strip())

    dictList.append(repInfo)

  for i in range(1, len(senateTable)):
    item = houseTable[i]
    repInfo = {}

    columns = item.find_all('td')
    link = columns[0].find('a')

    repInfo['Name'] = link.get_text().strip().replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Website'] = 'http://www.azleg.gov' + link.get('href')
    repInfo['District'] = 'AL State House District {0}'.format(columns[1].get_text().strip())
    repInfo['Party'] = partyDict[str(columns[2].get_text().strip())]
    repInfo['Email'] = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', columns[3].find('a').get('href'))
    repInfo['Address'] = '1700 West Washington, Room {0}, Phoenix, AZ 85007-2890'.format(columns[4].get_text().strip())
    repInfo['Phone'] = '(602)-{0}'.format(columns[5].get_text().strip())

    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getAZLeg(partyDict)

  with open('/home/michael/Desktop/AZLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      print row
      dwObject.writerow(row)

