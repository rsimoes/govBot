import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter


def getVTLeg(partyDict):
  buildingDict = {'LP': 'Legislative Plaza', 'WMB': 'War Memorial Building'}

  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.leg.state.vt.us/legdir/districts.cfm?Body=H').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.leg.state.vt.us/legdir/districts.cfm?Body=S').read(), 'lxml')
  
  houseTable = houseSoup.find('table', {'width': '790'}).find_all('tr')
  senateTable = senateSoup.find('table', {'width': '790'}).find_all('tr')

  dictList = []
  district = ''
  acceptNameRow = True
  acceptEmailRow = False

  for item in houseTable:
    distCell = item.find('td', {'align': re.compile('[Cc][Ee][Nn][Tt][Ee][Rr]')})
    columns = item.find_all('td')

    if distCell is not None:
      district = distCell.find('a').get_text().strip()
      repInfo = {}
      acceptNameRow = True
      acceptEmailRow = False
    elif len(columns) <= 1:
      repInfo = {}
      acceptNameRow = True
    elif item.find('td', {'align': 'RIGHT'}) and acceptNameRow:
      repInfo['District'] = 'VT State House District {0}'.format(district.title().replace('-', ' '))

      nameList = item.find('b').get_text().split(',')
      if len(nameList) == 2:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
      elif len(nameList) == 3:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[2].strip() + ' ' + nameList[0].strip()
      else:
        repInfo['Name'] = item.find('b').get_text().strip()
      acceptEmailRow = True
      acceptNameRow = False
    elif item.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]')}) and acceptEmailRow:
      repInfo['Email'] = item.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]')}).get_text().strip()
      acceptEmailRow = False

      dictList.append(repInfo)

  for item in senateTable:
    distCell = item.find('td', {'align': re.compile('[Cc][Ee][Nn][Tt][Ee][Rr]')})
    columns = item.find_all('td')

    if distCell is not None:
      district = distCell.find('a').get_text().replace('DISTRICT', '').strip()
      repInfo = {}
      acceptNameRow = True
      acceptEmailRow = False
    elif len(columns) <= 1:
      repInfo = {}
      acceptNameRow = True
    elif item.find('td', {'align': 'RIGHT'}) and acceptNameRow:
      repInfo['District'] = 'VT State Senate District {0}'.format(district.title().replace('-', ' '))

      nameList = item.find('b').get_text().split(',')
      if len(nameList) == 2:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
      elif len(nameList) == 3:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[2].strip() + ' ' + nameList[0].strip()
      else:
        repInfo['Name'] = item.find('b').get_text().strip()
      acceptEmailRow = True
      acceptNameRow = False
    elif item.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]')}) and acceptEmailRow:
      repInfo['Email'] = item.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]')}).get_text().strip()
      acceptEmailRow = False

      dictList.append(repInfo)


  return dictList

  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
  dictList = getVTLeg(partyDict)
  
  with open('/home/michael/Desktop/VTLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)