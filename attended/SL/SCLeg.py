import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getSCLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.scstatehouse.gov/member.php?chamber=H&order=D').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.scstatehouse.gov/member.php?chamber=S&order=D').read())
  
  houseTable = houseSoup.find('div', {'class': 'mainwidepanel'}).find_all('div', {'style': 'width: 325px; height: 135px; margin: 0 0 0 20px; text-align: left; float: left;'})
  senateTable = senateSoup.find('div', {'class': 'mainwidepanel'}).find_all('div', {'style': 'width: 325px; height: 135px; margin: 0 0 0 20px; text-align: left; float: left;'})

  dictList = []

  for item in houseTable:
    repInfo = {}
    link = item.find('a')
    if link is not None:
      namestring = link.string.strip()
      repInfo['Website'] = 'http://www.scstatehouse.gov' + link.get('href')
      repInfo['Name'] = re.sub(r'\[.*$','',link.string.strip()).strip().replace('   ', ' ').replace('  ', ' ')
      repInfo['Party'] = partyDict[str(re.sub(r'^.*\[(.*)\].*$', r'\1', link.string.strip()))]
    else:
      repInfo['Name'] = 'VACANT'

    repInfo['District'] = 'SC State House ' + re.sub(r'^.*(District [0-9]*).*$', r'\1', item.get_text())

    dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}
    link = item.find('a')
    if link is not None:
      namestring = link.string.strip()
      repInfo['Website'] = 'http://www.scstatehouse.gov' + link.get('href')
      repInfo['Name'] = re.sub(r'\[.*$','',link.string.strip()).strip().replace('   ', ' ').replace('  ', ' ')
      repInfo['Party'] = partyDict[str(re.sub(r'^.*\[(.*)\].*$', r'\1', link.string.strip()))]
    else:
      repInfo['Name'] = 'VACANT'

    repInfo['District'] = 'SC State Senate ' + re.sub(r'^.*(District [0-9]*).*$', r'\1', item.get_text())

    dictList.append(repInfo)
    
  return dictList
  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
  dictList = getSCLeg(partyDict)
  
  with open('/home/michael/Desktop/SCLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)
                                 
