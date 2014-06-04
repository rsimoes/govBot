import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getCTLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.cga.ct.gov/asp/menu/hlist.asp').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.cga.ct.gov/asp/menu/slist.asp').read())

  houseTable = houseSoup.find_all('tr',{'class': re.compile(r'(CGASVTableOdd)|(CGASVTableEven)')})
  senateTable = senateSoup.find_all('tr',{'class': re.compile(r'(CGASVTableOdd)|(CGASVTableEven)')})

  dictList = []

  for item in houseTable:
    repInfo = {}
    columns = item.find_all('td')
    
    rawIdent = columns[0].get_text().split('-')

    repInfo['District'] = 'CT State House District {0}'.format(int(rawIdent[0].strip()))

    rawName = rawIdent[1].split(',')
    if len(rawName) == 2:
      repInfo['Name'] = rawName[1].strip() + ' ' + rawName[0].strip()
    elif len(rawName) == 3:
      repInfo['Name'] = rawName[2].strip() + ' ' + rawName[0].strip() + ' ' + rawName[1].strip()
    else:
      repInfo['Name'] = rawIdent[1].strip()

    repInfo['Email'] = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', columns[1].find('a').get('href'))
    repInfo['Website'] = columns[2].find('a').get('href')
    repInfo['Party'] = partyDict[str(columns[3].get_text().strip())]

    dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}
    columns = item.find_all('td')
    
    rawIdent = columns[0].get_text().split('-')

    repInfo['District'] = 'CT State Senate District {0}'.format(int(rawIdent[0].strip()[1:]))

    rawName = rawIdent[1].split(',')
    if len(rawName) == 2:
      repInfo['Name'] = rawName[1].strip() + ' ' + rawName[0].strip()
    elif len(rawName) == 3:
      repInfo['Name'] = rawName[2].strip() + ' ' + rawName[0].strip() + ' ' + rawName[1].strip()
    else:
      repInfo['Name'] = rawIdent[1].strip()

    repInfo['Email'] = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', columns[1].find('a').get('href'))
    repInfo['Website'] = columns[2].find('a').get('href')
    repInfo['Party'] = partyDict[str(columns[3].get_text().strip())]

    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getCTLeg(partyDict)

  with open('/home/michael/Desktop/CTLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)