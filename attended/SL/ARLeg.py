import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getARLeg(partyDict):
  soup = BeautifulSoup(urllib2.urlopen('http://www.arkleg.state.ar.us/assembly/2013/2014F/Pages/LegislatorSearchResults.aspx?member=&committee=All&chamber=').read())

  dictList = []

  for i in range(135):
    repInfo={}
    row = soup.find('tr', {'id': 'ctl00_m_g_a01f6703_7388_46f6_95a3_a0e3b7cd3839_ctl00_gvMemberGrid_DXDataRow{0}'.format(i)})

    if row is not None:
      columns = row.find_all('td')
    link = columns[0].find('a')

    repInfo['Name'] = link.string.strip().replace('  ', ' ')
    repInfo['Website'] = link.get('href')
    repInfo['Email'] = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', columns[1].find('a').get('href'))

    repInfo['District'] = 'AR State {0} District {1}'.format(columns[2].string.strip(), columns[4].string.strip())

    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getARLeg(partyDict)

  with open('/home/michael/Desktop/ARLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)

