import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getALrep(url):
  print url
  email = ''
  response = urllib2.urlopen(url)

  if response.code == 200:
    soup = BeautifulSoup(response.read())

    tempEmail = soup.find('a', {'href': re.compile('mailto')})
    if tempEmail is not None:
      email = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', tempEmail.get('href'))

  return email


def getALLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.legislature.state.al.us/house/representatives/houseroster_alpha.html').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.legislature.state.al.us/senate/senators/senateroster_alpha.html').read())


  #These break and will periodically need to be adjusted. Alabama doesn't like classes or ID's, so hard-coded heights are the most useful/
  houseTable = houseSoup.find('table', {'height': '3374'}).find_all('tr')
  senateTable = senateSoup.find('table', {'height': '888'}).find_all('tr')

  dictList = []

  for i in range(1, len(houseTable)):
    repInfo = {}
    columns = houseTable[i].find_all('td')

    link = columns[0].find('a')

    if link.get('href') != '#':
      repInfo['Website'] = 'http://www.legislature.state.al.us/house/representatives/' + link.get('href')
      repInfo['Email'] = getALrep(repInfo['Website'])

    rawName = link.get_text().split(',')

    if len(rawName) == 2:
      repInfo['Name'] = rawName[1].strip().title() + ' ' + rawName[0].strip().title()
    elif len(rawName) == 3:
      repInfo['Name'] = rawName[1].strip().title() + ' ' + rawName[0].strip().title() + ' ' + rawName[2].strip().title()
    elif link.string is not None:
      repInfo['Name'] = link.string.strip().title()
    else:
      repInfo['Name'] = 'VACANT'

    repInfo['Name'] = repInfo['Name'].replace('Jr.', '').strip().replace('  ', ' ')
    repInfo['Party'] = partyDict[str(columns[1].get_text().strip())]
    repInfo['District'] = 'AL State House District {0}'.format(columns[2].get_text().replace('(','').replace(')','').strip())
    repInfo['Address'] = 'Room {0} 11 South Union Street Montomery, AL 36130'.format(columns[3].get_text().strip())
    repInfo['Phone'] = columns[4].get_text().strip()

    dictList.append(repInfo)

  for i in range(1, len(senateTable)):
    repInfo = {}
    columns = senateTable[i].find_all('td')

    link = columns[0].find('a')

    if link.get('href') != '#':
      repInfo['Website'] = 'http://www.legislature.state.al.us/senate/senators/' + link.get('href')
      repInfo['Email'] = getALrep(repInfo['Website'])

    rawName = link.get_text().split(',')

    if len(rawName) == 2:
      repInfo['Name'] = rawName[1].strip().title() + ' ' + rawName[0].strip().title()
    elif len(rawName) == 3:
      repInfo['Name'] = rawName[1].strip().title() + ' ' + rawName[0].strip().title() + ' ' + rawName[2].strip().title()
    elif link.string is not None:
      repInfo['Name'] = link.string.strip().title()
    else:
      repInfo['Name'] = ''

    repInfo['Name'] = repInfo['Name'].replace('Jr.', '').strip().replace('  ', ' ')
    repInfo['Party'] = partyDict[str(columns[1].get_text().strip())]
    repInfo['District'] = 'AL State Senate District {0}'.format(columns[2].get_text().strip())
    repInfo['Address'] = 'Room {0} 11 South Union Street Montomery, AL 36130'.format(columns[3].get_text().strip())
    repInfo['Phone'] = columns[4].get_text().strip()

    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getALLeg(partyDict)

  with open('/home/michael/Desktop/ALLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)

