import urllib2, urllib, re, xlrd, time
from bs4 import BeautifulSoup
from csv import DictWriter

def getNCRep(url):
  print url
  soup = BeautifulSoup(urllib2.urlopen(url).read())
  emailLink = soup.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]:')})
  email = ''

  if emailLink is not None:
    email = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', emailLink.get_text().strip())

  return email

def getNCLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.ncleg.net/gascripts/members/memberList.pl?sChamber=House').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.ncleg.net/gascripts/members/memberList.pl?sChamber=senate').read(), 'lxml')

  houseTable = houseSoup.find('table', {'width': '100%'}).find_all('tr')
  senateTable = senateSoup.find('table', {'width': '100%'}).find_all('tr')

  dictList = []

  for item in houseTable:
    repInfo = {}
    columns = item.find_all('td')\

    if len(columns) != 0:
      link = columns[2].find('a')

      repInfo['Name'] = link.get_text().strip().replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      repInfo['Website'] = 'http://www.ncleg.net' + link.get('href')
      repInfo['District'] = 'NC State House District {0}'.format(columns[1].get_text().strip())
      repInfo['Party'] = partyDict[str(columns[0].get_text().strip())]

      repInfo['Email'] = getNCRep(repInfo['Website'])

      dictList.append(repInfo)
  
  for item in senateTable:
    repInfo = {}
    columns = item.find_all('td')

    if len(columns) != 0:
      link = columns[2].find('a')

      repInfo['Name'] = link.get_text().strip().replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      repInfo['Website'] = 'http://www.ncleg.net' + link.get('href')
      repInfo['District'] = 'NC State Senate District {0}'.format(columns[1].get_text().strip())
      repInfo['Party'] = partyDict[str(columns[0].get_text().strip())]

      repInfo['Email'] = getNCRep(repInfo['Website'])

      dictList.append(repInfo)

  return dictList
  
if __name__ == "__main__":
  partyDict = {'Dem': 'Democratic', 'Rep': 'Republican', '(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getNCLeg(partyDict)
  
  with open('/home/michael/Desktop/NCLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)                                