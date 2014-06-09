import urllib2, urllib, re, xlrd, time
from bs4 import BeautifulSoup
from csv import DictWriter

def getMILeg(partyDict):
  soup = BeautifulSoup(urllib2.urlopen('http://www.legislature.mi.gov/(S(vqxrzp55ajyjbe55f02q0b55))/mileg.aspx?page=legislators').read(), 'lxml')
  tables = soup.find_all('table', {'class': 'indented'})[1].find_all('tr')[1].find_all('table')

  houseTable = tables[0].find_all('tr')
  senateTable = tables[1].find_all('tr')

  dictList = []

  for item in houseTable:
    repInfo = {}
    info = item.find_all('td')[1]

    repInfo['Name'] = info.find('b').get_text().strip()

    links = info.find_all('a')
    if str(links[0].get_text().strip()) == 'Web Page':
      repInfo['Website'] = links[0].get('href')
      repInfo['District'] = 'MI State House Unknown District'
    else:
      repInfo['District'] = 'MI State House District {0}'.format(links[0].get_text().strip())
      repInfo['Website'] = links[1].get('href')

    dictList.append(repInfo)
  
  for item in senateTable:
    repInfo = {}
    info = item.find_all('td')[1]

    repInfo['Name'] = info.find('b').get_text().strip()

    links = info.find_all('a')
    if str(links[0].get_text().strip()) == 'Web Page':
      repInfo['Website'] = links[0].get('href')
      repInfo['District'] = 'MI State Senate Unknown District'
    else:
      repInfo['District'] = 'MI State Senate District {0}'.format(links[0].get_text().strip())
      repInfo['Website'] = links[1].get('href')

    dictList.append(repInfo)

  return dictList
  
if __name__ == "__main__":
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getMILeg(partyDict)
  
  with open('/home/michael/Desktop/MILeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)                                