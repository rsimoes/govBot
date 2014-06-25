import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter


def getVALeg(partyDict):
  buildingDict = {'LP': 'Legislative Plaza', 'WMB': 'War Memorial Building'}

  houseSoup = BeautifulSoup(urllib2.urlopen('http://virginiageneralassembly.gov/house/members/members.php').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://apps.lis.virginia.gov/sfb1/Senate/TelephoneList.aspx').read(), 'lxml')
  
  houseTable = houseSoup.find('tbody').find_all('tr')
  senateTable = senateSoup.find('table', {'id': 'MainContent_TelephoneGridView'}).find_all('tr')

  dictList = []

  for item in houseTable:
    repInfo = {}
    columns = item.find_all('td')
    webID = re.sub(r'^.*\[([HS][0-9]*)\].*$', r'\1', item.get('id'))

    nameList = columns[0].get_text().split(',')
    if len(nameList) == 2:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
    elif len(nameList) == 3:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
    else:
      repInfo['Name'] = columns[0].get_text().strip()

    repInfo['District'] = 'VA State House District {0}'.format(re.sub(r'^.*?([0-9]*)[a-z]*.*$', r'\1', columns[1].get_text()))
    repInfo['Website'] = 'http://virginiageneralassembly.gov/house/members/members.php?id={0}'.format(webID)
    repInfo['Party'] = partyDict[str(columns[2].get_text().strip())]
    repInfo['Phone'] = columns[3].get_text().strip()
    repInfo['Email'] = columns[5].get_text().strip()

    dictList.append(repInfo)

  for item in senateTable:
    columns = item.find_all('td')
    repInfo = {}

    if len(columns) != 0:
      link = columns[0].find('a')

      nameList = link.get_text().split(',')
      if len(nameList) == 2:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
      elif len(nameList) == 3:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
      else:
        repInfo['Name'] = columns[0].get_text().strip()

      repInfo['District'] = 'VA State Senate District {0}'.format(columns[1].get_text().strip())
      repInfo['Website'] = 'http://apps.lis.virginia.gov/sfb1/Senate/' + link.get('href')
      repInfo['Party'] = partyDict[str(columns[2].get_text().strip())]
      repInfo['Phone'] = columns[3].get_text().strip()

      dictList.append(repInfo)

  return dictList

  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
  dictList = getVALeg(partyDict)
  
  with open('/home/michael/Desktop/VALeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)