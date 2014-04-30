import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

partyDict = {'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}

def getGASenate(wrtFile):
  soup = BeautifulSoup(urllib2.urlopen('http://www.senate.ga.gov/senators/en-US/SenateMembersList.aspx').read())
  table = soup.find('div', {'style': 'font-size:13px;'})
  firstCol = table.find_all('span', {'style': 'float:left; width:50%; border:1px solid #999999; border-bottom:0px; padding:3px;'})
  secondCol = table.find_all('span', {'style': 'float:left; width:15%; border:1px solid #999999; border-left:0px; border-bottom:0px; padding:3px;'})

  dictList = []

  for i in range(len(firstCol)):
    repInfo = {}
    nameInfo = firstCol[i].find('a')

    if nameInfo is not None:
      relativeWebsite = nameInfo.get('href')
      nameList = nameInfo.string.replace(")", "").replace("(",", ").split(",")
    else:
      relativeWebsite = firstCol[i].string.strip()
      nameList = firstCol[i].string.replace(")", "").replace("(",", ").split(",")

    checkDistrictLink = secondCol[i].find('a')

    if checkDistrictLink is not None:
      repInfo['District'] = 'GA State Senate District ' + checkDistrictLink.string.strip()
    else:
      repInfo['District'] = 'GA State Senate District ' + secondCol[i].string.strip()
    
    repInfo['Party'] = partyDict[str(nameList[len(nameList)-1].strip())]
    nameList.remove(nameList[len(nameList)-1])
    

    if len(nameList) == 2:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
    elif len(nameList) == 3:
      repInfo['Name'] = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
    else:
      repInfo['Name'] = ''
      for item in nameList:
        repInfo['Name'] = repInfo['Name'] + ' ' + item.strip()
      repInfo['Name'].strip()
      
    repInfo['Website'] = 'http://www.senate.ga.gov/senators/en-US' + re.sub("^\\.", "", relativeWebsite)
    dictList.append(repInfo)

  print len(dictList)
  with open(wrtFile, 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Website', 'Party'])
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)

  return dictList

if __name__ == '__main__':
  getGASenate('/home/michael/Desktop/GASenate.csv')
