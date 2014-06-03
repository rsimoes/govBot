import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getAKrep(url):
  print url
  soup = BeautifulSoup(urllib2.urlopen(url).read()).find('div', {'id': 'fullpage'})

  district = re.sub(r'^.*District: ([0-9A-Za-z]*).*$', r'\1', soup.get_text().replace('\n', ' '))
  party = re.sub(r'^.*Party: ([0-9A-Za-z]*).*$', r'\1', soup.get_text().replace('\n', ' '))

  email = ''
  tempEmail = soup.find('a', {'href': re.compile('mailto')})

  if tempEmail is not None:
    email = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', tempEmail.get('href'))

  return district, party, email


def getAKLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://house.legis.state.ak.us/').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://senate.legis.state.ak.us/').read())

  houseTable = houseSoup.find('div', {'id': 'legislators'}).find_all('div', {'class': 'leg_float'})
  senateTable = senateSoup.find('div', {'id': 'legislators'}).find_all('div', {'class': 'leg_float'})

  dictList = []

  for item in houseTable:
    repInfo = {}
    link = item.find('a')

    repInfo['Name'] = link.string.strip().replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Website'] = link.get('href')

    tempdist, tempparty, repInfo['Email'] = getAKrep(repInfo['Website'])

    repInfo['District'] = 'AK State House District ' + tempdist
    repInfo['Party'] = partyDict[str(tempparty)]

    dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}
    link = item.find('a')

    repInfo['Name'] = link.string.strip().replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Website'] = link.get('href')

    tempdist, tempparty, repInfo['Email'] = getAKrep(repInfo['Website'])
    
    repInfo['District'] = 'AK State Senate District ' + tempdist
    repInfo['Party'] = partyDict[str(tempparty)]

    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getAKLeg(partyDict)
  
  with open('/home/michael/Desktop/AKLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)

