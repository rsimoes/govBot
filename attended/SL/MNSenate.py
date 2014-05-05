import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

partyDict = {'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent', 'DFL': 'Democratic-Farmer Labor'}

def getMNSenate(wrtFile):
  soup = BeautifulSoup(urllib2.urlopen('http://www.senate.leg.state.mn.us/members/index.php?ls=#dist').read())
  table = soup.find('div', {'id': 'hide_show_alpha_all'})
  links = table.find_all('a')
  dictList = []

  for link in links:
    repInfo = {}
    if link.find('b') is not None:
      identity = link.find('b').string
      repInfo['District'] = 'MN State Senate District ' + str(int(identity.split("(")[1].split(",")[0].strip()))
      repInfo['Name'] = identity.split("(")[0].strip().replace("   ", " ").replace("  ", " ")
      repInfo['Party'] = partyDict[identity.split(',')[len(identity.split(','))-1].strip().replace(')','')]
      repInfo['Website'] = 'http://www.senate.leg.state.mn.us' + link.get('href')
      dictList.append(repInfo)

  print len(dictList)
  with open(wrtFile, 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Website', 'Party'])
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)

  return dictList

if __name__ == '__main__':
  getMNSenate('/home/michael/Desktop/MNSenate.csv')
