import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getTXRep(url, partyDict, body):
  print url
  soup = BeautifulSoup(urllib2.urlopen(url), 'lxml')
  distSpan = soup.find('span', {'id': 'lblDistrict'})

  district = ''
  name = ''
  phone = ''
  address = ''

  if distSpan is not None:
    district = 'TX State {0} District {1}'.format(body, distSpan.get_text().strip())
    name = re.sub(r'^.*(Rep\.|Sen\.)', '', soup.find('title').string.strip()).strip().replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    phone = soup.find('span', {'id': 'lblCapitolPhone'}).get_text().strip()
    address = '{0} {1}'.format(soup.find('span', {'id': 'lblCapitolAddress1'}).get_text().strip(), soup.find('span', {'id': 'lblCapitolAddress2'}).get_text().strip())

  return district, name, phone, address


def getTXLeg(partyDict):
  buildingDict = {'LP': 'Legislative Plaza', 'WMB': 'War Memorial Building'}

  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.capitol.state.tx.us/Members/Members.aspx?Chamber=H').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.capitol.state.tx.us/Members/Members.aspx?Chamber=S').read(), 'lxml')
  
  houseTable = houseSoup.find('table', {'id': 'dataListMembers'}).find_all('td')
  senateTable = senateSoup.find('table', {'id': 'dataListMembers'}).find_all('td')

  dictList = []

  for item in houseTable:
    repInfo = {}
    link = item.find('a')

    if link is not None:
      repInfo['Website'] = 'http://www.capitol.state.tx.us/Members/' + link.get('href')
      repInfo['District'], repInfo['Name'], repInfo['Phone'], repInfo['Address'] = getTXRep(repInfo['Website'], partyDict, 'House')

      dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}
    link = item.find('a')

    if link is not None:
      repInfo['Website'] = 'http://www.capitol.state.tx.us/Members/' + link.get('href')
      repInfo['District'], repInfo['Name'], repInfo['Phone'], repInfo['Address'] = getTXRep(repInfo['Website'], partyDict, 'Senate')

      dictList.append(repInfo)

  return dictList

  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
  dictList = getTXLeg(partyDict)
  
  with open('/home/michael/Desktop/TXLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)