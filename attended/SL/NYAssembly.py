import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getNYAssembly(partyDict):
  soup = BeautifulSoup(urllib2.urlopen('http://assembly.state.ny.us/mem/?sh=email').read())
  table = soup.find_all('div', {'class': re.compile('^email(1|2|3|clear)')})

  dictList = []
  repInfo = {}
 
  for item in table:
    
    if item.get('class') == [u'email1']:
      repInfo = {}
      nameString = item.string.strip().replace("    ", " ").replace("   ", " ").replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      nameList = nameString.split(',')

      if len(nameList) == 3:
        repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
      elif len(nameList) == 2:
        repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
      else:
        repInfo['Name'] = 'VACANT'
      if item.find('a') is not None:
        repInfo['Website'] = 'http://assembly.state.ny.us' + item.find('a').get('href')

    elif item.get('class') == [u'email2']:
      repInfo['District'] = 'NY State Assembly District ' + item.string.strip()[:len(item.string.strip())-2]
    
    elif item.get('class') == [u'email3']:
      if item is not None:
        if item.get('a') is not None:
          repInfo['Email'] = item.get('a').string

    else:
      dictList.append(repInfo)

  print len(dictList)

  return dictList

if __name__ == '__main__':
  partyDict = {'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent', 'DFL': 'Democratic-Farmer Labor'}
  dictList = getNYAssembly(partyDict)
  
  with open('/home/michael/Desktop/NYAssembly.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Website', 'Email'])
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)
