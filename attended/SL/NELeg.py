import urllib2, urllib, re, xlrd, time
from bs4 import BeautifulSoup
from csv import DictWriter

def getNERep(url):
  print url
  soup = BeautifulSoup(urllib2.urlopen(url).read())
  emailLink = soup.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]:')})
  email = ''

  if emailLink is not None:
    email = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', emailLink.get_text().strip())

  return email

def getNELeg(partyDict):
  soup = BeautifulSoup(urllib2.urlopen('http://nebraskalegislature.gov/senators/senator_list.php').read(), 'lxml')

  table = soup.find('table', {'width': '400px'}).find_all('tr')
  dictList = []

  for i in range(2, len(table)):
    item = table[i]
    repInfo = {}
    columns = item.find_all('td')

    link = columns[0].find('a')
    nameList = link.get_text().split(',')
    if len(nameList) == 2:
      name = nameList[1].strip() + ' ' + nameList[0].strip()
    elif len(nameList) == 3:
      name = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
    else:
      name = link.get_text().strip()

    repInfo['Name'] = name.replace(u'\u00A0', ' ').replace('   ', ' ').replace('  ', ' ').replace(u'\u0144','n').replace(u'\u00f1','n').replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
    repInfo['Website'] = link.get('href')
    repInfo['District'] = 'NE State House District {0}'.format(columns[1].get_text().strip())
    repInfo['Party'] = 'Nonpartisan'

    repInfo['Email'] = getNERep(repInfo['Website'])

    dictList.append(repInfo)

  return dictList
  
if __name__ == "__main__":
  partyDict = {'Dem': 'Democratic', 'Rep': 'Republican', '(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getNELeg(partyDict)
  
  with open('/home/michael/Desktop/NELeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)