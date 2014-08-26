import urllib2, urllib, re, xlrd, time
from bs4 import BeautifulSoup
from csv import DictWriter

def getMORep(url):
  while True:
    print url
    try:
      response = urllib2.urlopen(url, timeout = 10)
      soup = BeautifulSoup(response.read())
      emailLink = soup.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]:')})
      email = ''
      if emailLink is not None:
        email = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', emailLink.get_text().strip())
      return email
    except Exception:
      pass
  

def getMOLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.house.mo.gov/member.aspx').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.senate.mo.gov/14info/senateroster.htm').read(), 'lxml')

  houseTable = houseSoup.find('table', {'id': 'ContentPlaceHolder1_gridMembers_DXMainTable'}).find_all('tr', {'class': 'dxgvDataRow'})
  senateTable = senateSoup.find('table', {'width': '90%', 'border': '0'}).find_all('tr')

  dictList = []

  for item in houseTable:
    repInfo = {}

    columns = item.find_all('td', {'class': 'dxgv'})

    repInfo['District'] = 'MO State House District {0}'.format(int(columns[2].get_text().strip()))
    repInfo['Party'] = partyDict[str(columns[3].get_text().strip())]
    repInfo['Name'] = '{0} {1}'.format(columns[1].get_text().strip(), columns[0].get_text().strip()).strip()
    repInfo['Website'] = 'http://www.house.mo.gov/member.aspx?year=2014&district=' + columns[2].get_text().strip()
    repInfo['Phone'] = columns[4].get_text().strip()
    repInfo['Address'] = '201 West Capitol Avenue Room {0} Jefferson City, MO 65101'.format(columns[5].get_text().strip())

    repInfo['Email'] = getMORep(repInfo['Website'])    

    dictList.append(repInfo)
  
  for i in range(1, len(senateTable)):
    item = senateTable[i]
    repInfo = {}

    columns = item.find_all('td')
    link = columns[0].find('a')
    listPartyDist = columns[1].get_text().split('-')

    repInfo['Name'] = link.get_text().strip()
    repInfo['Website'] = link.get('href')

    if len(listPartyDist) == 2:
      repInfo['District'] = 'MO State Senate District {0}'.format(listPartyDist[1].strip())
      repInfo['Party'] = partyDict[str(listPartyDist[0].strip())]
    else:
      repInfo['District'] = 'MO State Senate District {0}'.format(listPartyDist[0].strip())
      repInfo['Party'] = 'Unknown'

    repInfo['Phone'] = columns[3].get_text().strip()
    repInfo['Address'] = '201 West Capitol Avenue Room {0} Jefferson City, MO 65101'.format(columns[2].get_text().strip())

    dictList.append(repInfo)
  return dictList
  
if __name__ == "__main__":
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getMOLeg(partyDict)
  
  with open('/home/michael/Desktop/MOLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)                                