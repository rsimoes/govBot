import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter


def getWILeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://legis.wisconsin.gov/Pages/leg-list.aspx?h=a').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://legis.wisconsin.gov/Pages/leg-list.aspx?h=s').read(), 'lxml')
  
  houseTable = houseSoup.find_all('div', {'class': re.compile('rounded')})
  senateTable = senateSoup.find_all('div', {'class': re.compile('rounded')})

  dictList = []

  for i in range(1, len(houseTable)):
    repInfo = {}
    columns = houseTable[i].find('span', {'class': 'info'}).find_all('span')
    smallTags = houseTable[i].find_all('small')
    
    if len(columns) > 1:
      link = columns[0].find('strong').find('a')

      identityText = link.get_text().replace('\n', ' ').strip()
      nameText = re.sub(r'^(.*)\(.*$', r'\1', identityText)

      nameList = nameText.split(',')
      if len(nameList) == 2:
        name = nameList[1].strip() + ' ' + nameList[0].strip()
      elif len(nameList) == 3:
        name = nameList[1].strip() + ' ' + nameList[2].strip() + ' ' + nameList[0].strip()
      else:
        name = nameText.strip()

      repInfo['Name'] = name.replace(u'\u00A0', ' ').strip().replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      repInfo['Website'] = link.get('href')

      if re.search('Details', columns[2].get_text()):
        repInfo['District'] = 'WI State Assembly {0}'.format(columns[1].get_text().strip())
      else:
        repInfo['District'] = 'WI State Assembly {0}'.format(columns[2].get_text().strip())
      
      partyText = columns[0].find('small')
      if partyText is not None:
        repInfo['Party'] = partyDict[str(partyText.get_text()[1])]

      dictList.append(repInfo)

  for i in range(1, len(senateTable)):
    repInfo = {}
    columns = senateTable[i].find('span', {'class': 'info'}).find_all('span')

    if len(columns) > 1:
      link = columns[0].find('strong').find('a')

      identityText = link.get_text().replace('\n', ' ').strip()
      nameText = re.sub(r'^(.*)\(.*$', r'\1', identityText)

      nameList = nameText.split(',')
      if len(nameList) == 2:
        name = nameList[1].strip() + ' ' + nameList[0].strip()
      elif len(nameList) == 3:
        name = nameList[1].strip() + ' ' + nameList[2].strip() + ' ' + nameList[0].strip()
      else:
        name = nameText.strip()

      repInfo['Name'] = name.replace(u'\u00A0', ' ').strip().replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      repInfo['Website'] = link.get('href')

      if re.search('Details', columns[2].get_text()):
        repInfo['District'] = 'WI State Senate {0}'.format(columns[1].get_text().strip())
      else:
        repInfo['District'] = 'WI State Senate {0}'.format(columns[2].get_text().strip())

      partyText = columns[0].find('small')
      if partyText is not None:
        repInfo['Party'] = partyDict[str(partyText.get_text()[1])]

      dictList.append(repInfo)

  return dictList

  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent', 'Republican': 'Republican', 'Democrat': 'Democratic'}
  dictList = getWILeg(partyDict)
  
  with open('/home/michael/Desktop/WILeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)