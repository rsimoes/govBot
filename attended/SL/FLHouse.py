import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getFLHouse(partyDict):
  soup = BeautifulSoup(urllib2.urlopen('http://www.myfloridahouse.gov/Sections/Representatives/representatives.aspx?SortField=district&SortDirection=asc&LegislativeTermId=85&LastSortField=Name').read())
  rawReps = soup.find_all('div', {'class': 'rep_style'})
  rawDistricts = soup.find_all('div', {'class': 'district_style'})
  rawParties = soup.find_all('div', {'class': 'party_style'})
  rawTerms = soup.find_all('div', {'class': 'term_style'})
  dictList = []


  if len(rawReps) == len(rawDistricts) == len(rawParties) == len(rawTerms):
    for i in range(len(rawReps)):
      repDict = {}
      rep = rawReps[i]
      district = rawDistricts[i].string.replace(" ", "").strip()
      party = rawParties[i].string.replace(" ", "").strip()
      term = rawTerms[i]
      website = 'http://www.myfloridahouse.gov' + rep.find('a').get('href')
      nameList = rep.find('a').string.split(',')

      if len(nameList) == 2:
        name = nameList[1].strip() + ' ' + nameList[0].strip()
      elif len(nameList) > 2:
        name = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList [1].strip() 
      else:
        name = rep.find('a').string.strip()   

      name = name.encode('utf-8', 'replace').replace('   ', ' ').replace('  ', ' ')
      
      repDict['Name'] = name
      repDict['District'] = 'FL State House District ' + district
      repDict['Party'] = partyDict[party]
      repDict['Website'] = website
      dictList.append(repDict)

  return dictList

if __name__ ==  '__main__':
  partyDict = {'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent'}
  dictList = getFLHouse(partyDict)

  with open('/home/michael/Desktop/FLHouse.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website'])
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)
