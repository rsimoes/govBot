import urllib2, urllib, re, xlrd,time
from bs4 import BeautifulSoup
from csv import DictWriter

def getKYRep(url, partyDict):
  print url

  check = True
  html = ''

  while check:
    try:
      response = urllib2.urlopen(url, timeout=2)
      if response.code == 200:
        html = response.read().replace('<br>', ' ').replace('<BR>', ' ').replace('<br />', ' ').replace('<BR />', ' ').replace('<br/>', ' ').replace('<BR/>', ' ')
        check = False
    except:
      pass

  soup = BeautifulSoup(html, 'lxml')

  for element in soup.find_all('br'):
    element.extract()

  email = ''
  address = ''

  party = partyDict[str(re.sub(r'^.*\((.)\).*$', r'\1', soup.find('span', {'id': 'name'}).get_text()))]
  
  emailLink = soup.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]:')})
  rawAddress = soup.find('div', {'id': 'MailingAddress'})

  if emailLink is not None:
    email = re.sub(r'^.*[Mm][Aa][Ii][Ll][Tt][Oo]:(.*)$', r'\1', emailLink.get('href'))
  if rawAddress is not None:
    address = rawAddress.find('span', {'class': 'bioText'}).get_text().replace('\n', ' ').strip()

  return party, address, email

def getKYLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.lrc.ky.gov/whoswho/hsedist.htm').read(), 'lxml')
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.lrc.ky.gov/whoswho/sendist.htm').read(), 'lxml')

  houseTable = houseSoup.find('table', {'id': 'innerTable'}).find_all('tr')
  senateTable = senateSoup.find('table', {'id': 'innerTable'}).find_all('tr')

  dictList = []

  for i in range(1, len(houseTable)):
    repInfo = {}
    columns = houseTable[i].find_all('td')
    link = columns[1].find('a')

    nameList = link.get_text().split(',')
    if len(nameList) == 2:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
    elif len(nameList) == 2:
      repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
    else:
      repInfo['Name'] = link.get_text().strip()

    repInfo['District'] = 'KY State House District {0}'.format(columns[0].get_text().strip())
    repInfo['Website'] = link.get('href')

    repInfo['Party'], repInfo['Address'], repInfo['Email'] = getKYRep(repInfo['Website'], partyDict)

    dictList.append(repInfo)
  
  for i in range(1, len(senateTable)):
    repInfo = {}
    columns = senateTable[i].find_all('td')
    link = columns[1].find('a')

    nameList = link.get_text().split(',')
    if len(nameList) == 2:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
    elif len(nameList) == 2:
      repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
    else:
      repInfo['Name'] = link.get_text().strip()

    repInfo['District'] = 'KY State Senate District {0}'.format(columns[0].get_text().strip())
    repInfo['Website'] = link.get('href')

    repInfo['Party'], repInfo['Address'], repInfo['Email'] = getKYRep(repInfo['Website'], partyDict)
  
    dictList.append(repInfo)

  return dictList
  
if __name__ == "__main__":
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getKYLeg(partyDict)
  
  with open('/home/michael/Desktop/KYLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)                                