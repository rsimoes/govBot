import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getCALeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://assembly.ca.gov/assemblymembers').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://senate.ca.gov/senators').read())

  houseTable = houseSoup.find('tbody').find_all('tr')
  senateTable = senateSoup.find_all('div', {'class': re.compile('views-row')})

  dictList = []

  for item in houseTable:
    repInfo = {}

    columns = item.find_all('td')
    link = item.find('td', {'class': 'views-field views-field-field-member-lname-value-1'}).find('a')

    if link is None:
      repInfo['Name'] = item.find('td', {'class': 'views-field views-field-field-member-lname-value-1'}).get_text().strip()
    else:
      rawName = link.get_text().split(',')
      if len(rawName) == 2:
        repInfo['Name'] = rawName[1].strip() + ' ' + rawName[0].strip().replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      elif len(rawName) == 3:
        repInfo['Name'] = rawName[2].strip() + ' ' + rawName[0].strip() + ' ' + rawName[1].strip().replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      else:
        repInfo['Name'] = link.get_text().strip().replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')

      repInfo['Website'] = link.get('href')
    repInfo['District'] = 'CA State Assembly District {0}'.format(item.find('td', {'class': 'views-field views-field-field-member-district-value'}).get_text().strip())
    repInfo['Party'] = partyDict[str(item.find('td', {'class': 'views-field views-field-field-member-party-value'}).get_text().strip())]

    rawContact = item.find('td', {'class': 'views-field views-field-field-member-feedbackurl-value'}).find('p').get_text().split(';')
    repInfo['Phone'] = rawContact[1].strip()
    repInfo['Address'] = rawContact[0].strip()

    dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}

    rawDist = item.find('span', {'class': 'district-number'}).get_text().strip()
    repInfo['District'] = 'CA State Senate District {0}'.format(int(rawDist[len(rawDist)-3:]))

    identInfo = item.find('li')
    rawName = identInfo.find('h2').get_text().strip()

    if str(rawName.strip()[:8]) == 'District':
      repInfo['Name'] = 'VACANT'
    else:
      repInfo['Name'] = re.sub(r'^(.*) \(.\)$', r'\1', rawName).replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      if re.search('\(.*\)', rawName):
        repInfo['Party'] = partyDict[str(re.sub(r'^.*\((.)\)$', r'\1', rawName))]

    repInfo['Website'] = identInfo.find('a').get('href')

    rawContact = item.find('div', {'class': 'views-field-field-senate-offices-value'}).find('p').get_text().split(';')
    repInfo['Phone'] = rawContact[1].strip()
    repInfo['Address'] = rawContact[0].strip().replace(u'\u00A0', ' ')

    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getCALeg(partyDict)

  with open('/home/michael/Desktop/CALeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      print row
      dwObject.writerow(row)

