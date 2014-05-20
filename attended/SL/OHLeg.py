import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getOHLeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.ohiohouse.gov/members/member-directory').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.ohiosenate.gov/members/senate-directory').read())

  dictList = []

  houseTable = houseSoup.find_all('div', {'class': 'data'})  
  senateTable = senateSoup.find_all('div', {'class': 'memberModule'})

  for item in houseTable:
    repInfo = {}
    nameLink = item.find('a', {'class':'black'})
    
    repInfo['Name'] = nameLink.string.strip().replace(u'\u00a0', ' ').replace('   ', ' ').replace('  ', ' ')
    repInfo['Website'] = nameLink.get('href').replace('..', 'http://www.ohiohouse.gov')
    repInfo['Party'] = partyDict[item.find('span', {'class': 'partyLetter'}).string]

    contactList = str(item).replace('</h3>', '<br/>').split('<br/>')

    repInfo['District'] = 'OH State House ' + contactList[1]
    
    for i in range(len(contactList)-2):
      if re.search(r'^\([0-9]*\)', contactList[i+2]):
        repInfo['Address'] = contactList[i-1] + ' ' + contactList[i] + ' ' + contactList[i+1]
        repInfo['Phone'] = contactList[i+2]

    dictList.append(repInfo)

  for largeItem in senateTable:
    repInfo = {}
    item = largeItem.find('div', {'class': 'data'})
    nameLink = item.find('a', {'class':'black'})
    
    repInfo['Name'] = nameLink.string.strip().replace(u'\u00a0', ' ').replace('   ', ' ').replace('  ', ' ')
    repInfo['Website'] = nameLink.get('href').replace('..', 'http://www.ohiosenate.gov')
    repInfo['Party'] = partyDict[item.find('span', {'class': 'partyLetter'}).string]

    contactList = str(item).split('<br/>')

    for i in range(len(contactList)-1):
      if re.search(r'^\([0-9]*\)', contactList[i+1]):
        repInfo['Address'] = contactList[i-2] + ' ' + contactList[i-1] + ' ' + contactList[i]
        repInfo['Phone'] = contactList[i+1]
    
    distNumber = re.sub(r'^.*MemberModuleBackgrounds/([0-9]*)\.png.*$', r'\1', largeItem.get('style'))
    repInfo['District'] = 'OH State Senate District ' + distNumber
    
    dictList.append(repInfo)
    
  return dictList
  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
  dictList = getOHLeg(partyDict)
  
  with open('/home/michael/Desktop/OHLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)
                                 
