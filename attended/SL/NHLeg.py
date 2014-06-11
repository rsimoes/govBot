import urllib2, urllib, re, xlrd, time
from bs4 import BeautifulSoup
from csv import DictWriter, DictReader
from StringIO import StringIO

def getNHLeg(partyDict):
  houseText = urllib2.urlopen('http://www.gencourt.state.nh.us/downloads/Members.txt').read()
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.gencourt.state.nh.us/senate/members/senate_roster.aspx').read(), 'lxml')

  houseTable = DictReader(StringIO(houseText), delimiter = '\t', fieldnames = ['chamber', 'fullName', 'lastName', 'firstName', 'middleName', 'town', 'district', 'id', 'party', 'street1', 'street2', 'city', 'state', 'zip', 'phone', 'home', 'cell', 'email', 'committees', 'committees2', 'committees3'])
  senateTable = senateSoup.find('table', {'id': 'nhsenators'}).find_all('tr')

  dictList = []

  for item in houseTable:
    repInfo = {}
    print item
    repInfo['District'] = 'NH State {0} District {1} {2}'.format(item['chamber'], item['town'], item['district'])
    repInfo['Party'] = partyDict[str(item['party'])]
    repInfo['Name'] = '{0} {1} {2}'.format(item['firstName'], item['middleName'], item['lastName']).strip().replace('    ', ' ').replace('  ', ' ').replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Phone'] = item['phone']
    repInfo['Address'] = '{0} {1} {2}, {3} {4}'.format(item['street1'], item['street2'], item['city'], item['state'], item['zip']).replace('   ', ' ').replace('  ', ' ')
    repInfo['Email'] = item['email']  

    dictList.append(repInfo)
  
  for item in senateTable:
    repInfo = {}

    if len(item.find_all('td')) > 1:
      identity = item.find('td', {'style': 'width:35%'}).find('b').get_text().replace('\n', ' ').replace('\r', ' ').strip()

      repInfo['Name'] = re.sub(r'^(.*)\(.*?$', r'\1', identity).replace(u'\u00A0', ' ').strip().replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      repInfo['Website'] = item.find('a', {'href': re.compile('webpages/')}).get('href')
      repInfo['Party'] = partyDict[str(re.sub(r'^.*\((.)\).*?$', r'\1', identity))]
      repInfo['Email'] = item.find('email_address').get_text().strip()
      repInfo['District'] = 'NH State Senate District {0}'.format(int(item.find('districtno').get_text().strip()))

      dictList.append(repInfo)

  return dictList
  
if __name__ == "__main__":
  partyDict = {'d+r': 'Unknown', 'd': 'Democratic', 'r': 'Republican', '(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getNHLeg(partyDict)
  
  with open('/home/michael/Desktop/NHLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)