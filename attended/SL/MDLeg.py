import urllib2, urllib, re, xlrd,time
from bs4 import BeautifulSoup
from csv import DictWriter

def getMDRep(url, partyDict):
  print url
  soup = BeautifulSoup(urllib2.urlopen(url).read())

  table = soup.find('table', {'class': 'spco'}).find_all('tr')
  emailLink = table[2].find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]:')})

  email = ''
  party = table[5].find('td').get_text().strip()

  if emailLink is not None:
    email = emailLink.get_text().strip()

  return party, email

def getMDLeg(partyDict):
  soup = BeautifulSoup(urllib2.urlopen('http://www.mgaleg.maryland.gov/webmga/frmmain.aspx?pid=legisrpage&tab=subject6').read(), 'lxml')
  tables = soup.find_all('table', {'class': 'grid'})

  houseTable = tables[1].find_all('tr')
  senateTable = tables[0].find_all('tr')

  repParties = {}
  dictList = []

  for i in range(1, len(houseTable)):
    item = houseTable[i]
    repInfo = {}
    columns = item.find_all('td')
    link = columns[0].find('a')
    name = ''

    rawName = link.get_text().strip()
    nameList = rawName.split(',')
    if len(nameList) == 2:
      name = nameList[1].strip() + ' ' + nameList[0].strip()
    elif len(nameList) == 3:
      name = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
    else:
      name = rawName

    repInfo['Name'] = name.replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['District'] = 'MD State House District {0}'.format(columns[1].get_text().strip())
    repInfo['Website'] = 'http://www.mgaleg.maryland.gov/webmga/' + link.get('href').replace('..', '')
    repInfo['Party'], repInfo['Email'] = getMDRep(repInfo['Website'], partyDict)

    dictList.append(repInfo)
  
  for i in range(1, len(senateTable)):
    item = senateTable[i]
    repInfo = {}
    columns = item.find_all('td')
    link = columns[0].find('a')
    name = ''

    rawName = link.get_text().strip()
    nameList = rawName.split(',')
    if len(nameList) == 2:
      name = nameList[1].strip() + ' ' + nameList[0].strip()
    elif len(nameList) == 3:
      name = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
    else:
      name = rawName

    repInfo['Name'] = name.replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['District'] = 'MD State Senate District {0}'.format(columns[1].get_text().strip())
    repInfo['Website'] = 'http://www.mgaleg.maryland.gov/webmga/' + link.get('href').replace('..', '')
    repInfo['Party'], repInfo['Email'] = getMDRep(repInfo['Website'], partyDict)

    dictList.append(repInfo)
  return dictList
  
if __name__ == "__main__":
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getMDLeg(partyDict)
  
  with open('/home/michael/Desktop/MDLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)                                