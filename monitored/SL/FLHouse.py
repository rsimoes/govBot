import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

partyDict = {'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent'}

def getFLHouse(wrtFile):
  soup = BeautifulSoup(urllib2.urlopen('http://www.myfloridahouse.gov/Sections/Representatives/representatives.aspx?SortField=district&SortDirection=asc&LegislativeTermId=85&LastSortField=name').read())
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
      dictList.append(repDict)

  print len(dictList)
  with open(wrtFile, 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party'])
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)

if __name__ == '__main__':
  getFLHouse('/home/michael/Desktop/FLHouse.csv')
