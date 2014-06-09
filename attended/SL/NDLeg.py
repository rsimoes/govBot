import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getNDLeg(partyDict):
  soup = BeautifulSoup(urllib2.urlopen('http://www.legis.nd.gov/assembly/63-2013/members/').read())
  
  firstMember = soup.find_all('div', {'class': 'member-img-list first odd'})
  oddMembers = soup.find_all('div', {'class': 'member-img-list odd'})
  evenMembers = soup.find_all('div', {'class': 'member-img-list even'})
  lastMember = soup.find_all('div', {'class': 'member-img-list last odd'})
  table = firstMember + oddMembers + evenMembers + lastMember

  dictList = []
  
  for rep in table:
    repInfo = {}
    body = rep.find('div', {'class': 'chamber'}).string.strip()
    district = rep.find('div', {'class': 'district'}).find('a').string.strip()
    nameLink = rep.find('div', {'class': 'name'}).find('a')
    nameList = nameLink.string.split(',')

    if len(nameList) == 3:
      repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
    else:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()

    repInfo['District'] = 'ND State ' + body + ' ' + district
    repInfo['Website'] = nameLink.get('href')
    repInfo['Party'] =rep.find('div', {'class': 'party'}).string.strip()
    
    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}

  getNDLeg(partyDict)

  with open('/home/michael/Desktop/NDLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)
