import urllib2, urllib, re, xlrd, time
from bs4 import BeautifulSoup
from csv import DictWriter

def getNMRep(url, partyDict):
  print url
  soup = BeautifulSoup(urllib2.urlopen(url).read())

  identity = soup.find('span', {'id': 'ctl00_mainCopy_formViewLegislator_lblHeader'}).get_text().strip()
  party = partyDict[str(re.sub(r'^.*\((.)\).*?$', r'\1', identity))]

  rawEmail = soup.find('a', {'id': 'ctl00_mainCopy_formViewLegislator_linkEmail'})
  rawPhone = soup.find('span', {'id': 'ctl00_mainCopy_formViewLegislator_lblCapitolPhone'})
  rawAddress = soup.find('span', {'id': 'ctl00_mainCopy_formViewLegislator_lblAddress'})

  email = ''
  phone = ''
  address = ''

  if rawEmail is not None:
    email = rawEmail.get_text().strip()
  if rawPhone is not None:
    phone = '(505) ' + rawPhone.get_text().strip()
  if rawAddress is not None:
    address = rawAddress.get_text().strip()

  return party, email, phone, address


def getNMLeg(partyDict):
  soup = BeautifulSoup(urllib2.urlopen('http://www.nmlegis.gov/lcs/districts.aspx').read(), 'lxml')

  houseTable = soup.find('table', {'id': 'ctl00_mainCopy_gridViewHouseDistricts'})
  senateTable = soup.find('table', {'id': 'ctl00_mainCopy_gridViewSenateDistricts'})
  dictList = []

  for i in range(2, 72):
    repInfo = {}

    repInfo['District'] = 'NM State House District {0}'.format(houseTable.find('span', {'id': 'ctl00_mainCopy_gridViewHouseDistricts_ctl{0}_lblDistrict'.format("%02d" % i)}).get_text().strip())
    
    name = houseTable.find('span', {'id': 'ctl00_mainCopy_gridViewHouseDistricts_ctl{0}_lblFirstName'.format("%02d" % i)}).get_text().strip() + ' ' + houseTable.find('span', {'id': 'ctl00_mainCopy_gridViewHouseDistricts_ctl{0}_lblLastName'.format("%02d" % i)}).get_text().strip()

    repInfo['Name'] = name.encode('latin1').decode('utf8').replace(u'\u00A0', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Website'] = 'http://www.nmlegis.gov/lcs/' + houseTable.find('a', {'id': 'ctl00_mainCopy_gridViewHouseDistricts_ctl{0}_linkSponsor'.format("%02d" % i)}).get('href')

    repInfo['Party'], repInfo['Email'], repInfo['Phone'], repInfo['Address'] = getNMRep(repInfo['Website'], partyDict)
    dictList.append(repInfo)

    if i <= 43:
      repInfo = {}

      repInfo['District'] = 'NM State Senate District {0}'.format(senateTable.find('span', {'id': 'ctl00_mainCopy_gridViewSenateDistricts_ctl{0}_lblDistrict'.format("%02d" % i)}).get_text().strip())
    
      name = senateTable.find('span', {'id': 'ctl00_mainCopy_gridViewSenateDistricts_ctl{0}_lblFirstName'.format("%02d" % i)}).get_text().strip() + ' ' + senateTable.find('span', {'id': 'ctl00_mainCopy_gridViewSenateDistricts_ctl{0}_lblLastName'.format("%02d" % i)}).get_text().strip()

      repInfo['Name'] = name.encode('latin1').decode('utf8').replace(u'\u00A0', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      repInfo['Website'] = 'http://www.nmlegis.gov/lcs/' + senateTable.find('a', {'id': 'ctl00_mainCopy_gridViewSenateDistricts_ctl{0}_linkSponsor'.format("%02d" % i)}).get('href')

      repInfo['Party'], repInfo['Email'], repInfo['Phone'], repInfo['Address'] = getNMRep(repInfo['Website'], partyDict)

      dictList.append(repInfo)

  return dictList

  
if __name__ == "__main__":
  partyDict = {'Dem': 'Democratic', 'Rep': 'Republican', '(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getNMLeg(partyDict)
  
  with open('/home/michael/Desktop/NMLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)