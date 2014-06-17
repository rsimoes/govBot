import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter


def getWVLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.legis.state.wv.us/House/roster.cfm').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.legis.state.wv.us/Senate1/roster.cfm').read(), 'lxml')
  
  houseTable = houseSoup.find('table', {'class': 'tabborder'}).find_all('tr', {'valign': 'top'})
  senateTable = senateSoup.find('table', {'class': 'tabborder'}).find_all('tr', {'valign': 'top'})

  dictList = []

  for item in houseTable:
    repInfo = {}

    columns = item.find_all('td')
    link = columns[0].find('a', {'style': 'vertical-align:top'})

    repInfo['Name'] = link.get_text().replace(u'\u00A0', ' ').strip().replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Website'] = 'http://www.legis.state.wv.us/House/' + link.get('href')
    repInfo['Party'] = partyDict[str(columns[1].get_text().strip())]
    repInfo['District'] = 'WV State House District {0}'.format(int(columns[2].get_text().strip()))
    repInfo['Email'] = columns[4].get_text().strip()
    repInfo['Phone'] = columns[5].get_text().strip()
    repInfo['Address'] = columns[3].get_text().strip()

    dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}

    columns = item.find_all('td')
    link = columns[0].find('a', {'style': 'vertical-align:top'})

    repInfo['Name'] = link.get_text().replace(u'\u00A0', ' ').strip().replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Website'] = 'http://www.legis.state.wv.us/Senate1/' + link.get('href')
    repInfo['Party'] = partyDict[str(columns[1].get_text().strip())]
    repInfo['District'] = 'WV State Senate District {0}'.format(int(columns[2].get_text().strip()))
    repInfo['Email'] = columns[4].get_text().strip()
    repInfo['Phone'] = columns[5].get_text().strip()
    repInfo['Address'] = columns[3].get_text().strip()

    dictList.append(repInfo)

  return dictList

  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent', 'Republican': 'Republican', 'Democrat': 'Democratic'}
  dictList = getWVLeg(partyDict)
  
  with open('/home/michael/Desktop/WVLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)