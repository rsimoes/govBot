import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter


def getUTLeg(partyDict):
  buildingDict = {'LP': 'Legislative Plaza', 'WMB': 'War Memorial Building'}

  houseSoup = BeautifulSoup(urllib2.urlopen('http://le.utah.gov/house2/representatives.jsp').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.utahsenate.org/aspx/roster.aspx').read(), 'lxml')
  
  houseTable = houseSoup.find('table').find_all('tr')
  senateTable = senateSoup.find('table', {'id': 'rosterTable'}).find_all('tr')

  dictList = []

  for item in houseTable:
    repInfo = {}
    columns = item.find_all('td')

    if len(columns) > 0:
      link = columns[1].find('a')
      nameList = link.get_text().split(',')

      if len(nameList) == 2:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
      elif len(nameList) == 3:
        repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + nameList[1].strip()
      else:
        repInfo['Name'] = link.get_text().strip()

      repInfo['Website'] = 'http://le.utah.gov/house2/' + link.get('href')
      repInfo['District'] = 'UT State House District {0}'.format(columns[0].get_text().strip())
      repInfo['Party'] = partyDict[str(columns[2].get_text().strip())]
      repInfo['Email'] = columns[4].find('a').get_text().strip()
      repInfo['Phone'] = columns[4].get_text().replace(repInfo['Email'], '').strip()

      dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}
    columns = item.find_all('td')

    if len(columns) > 0:
      link = columns[2].find('a')
      nameList = link.get_text().split(',')

      if len(nameList) == 2:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
      elif len(nameList) == 3:
        repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + nameList[1].strip()
      else:
        repInfo['Name'] = link.get_text().strip() 

      repInfo['District'] = 'UT State Senate District {0}'.format(columns[0].get_text().strip())
      repInfo['Website'] = 'http://www.utahsenate.org/aspx/' + link.get('href')
      repInfo['Party'] = partyDict[str(re.sub(r'^.*\((.)\).*$', r'\1', columns[2].get_text()))]
      repInfo['Email'] = columns[2].find('span', {'class': 'email'}).find('a').get_text().strip()
      repInfo['Address'] = columns[3].get_text().strip()
      repInfo['Phone'] = re.sub(r'^.*([0-9]{3}-[0-9]{3}-[0-9]{4}).*$', r'\1', columns[4].get_text())

      dictList.append(repInfo)



  return dictList

  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
  dictList = getUTLeg(partyDict)
  
  with open('/home/michael/Desktop/UTLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)