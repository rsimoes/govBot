import urllib2, re
from bs4 import BeautifulSoup
from csv import DictWriter

def getDERep(url, partyDict):
  print url
  soup = BeautifulSoup(urllib2.urlopen(url).read())

  email = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', soup.find('td', {'width': '281'}).find('a').get('href'))
  party = partyDict[re.sub(r'^.*\((.)\).*$', r'\1', soup.find('td', {'width': '120'}).get_text().strip().replace('\n', ' '))]

  contacts = soup.find('td', {'width': '152'}).find_all('font')
  address = 'P.O. Box 1401 Legislative Hall Dover, DE 19903'
  phone = re.sub(r'^.*? (.*)$', r'\1', contacts[1].get_text().strip().split('\n')[0]).strip()

  return party, phone, address, email


def getDELeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://legis.delaware.gov/legislature.nsf/Reps?openview&count=75&nav=contact').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://legis.delaware.gov/legislature.nsf/Sen?openview&nav=contact').read())

  houseTable = houseSoup.find('table', {'cellpadding': '2'}).find_all('tr',{'valign': 'top'})
  senateTable = senateSoup.find('table', {'cellpadding': '2'}).find_all('tr',{'valign': 'top'})

  dictList = []

  for item in houseTable:
    repInfo = {}

    columns = item.find_all('td')
    link = columns[0].find('a')

    repInfo['Website'] = 'http://legis.delaware.gov' + link.get('href')
    repInfo['Name'] = link.get_text().strip().replace('  ', ' ')
    repInfo['District'] = 'DE State House District {0}'.format(columns[2].get_text().strip())

    repInfo['Party'], repInfo['Phone'], repInfo['Address'], repInfo['Email'] = getDERep(repInfo['Website'], partyDict)

    dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}

    columns = item.find_all('td')
    link = columns[0].find('a')

    repInfo['Website'] = 'http://legis.delaware.gov' + link.get('href')
    repInfo['Name'] = link.get_text().strip().replace('  ', ' ')
    repInfo['District'] = 'DE State Senate District {0}'.format(columns[2].get_text().strip())

    repInfo['Party'], repInfo['Phone'], repInfo['Address'], repInfo['Email'] = getDERep(repInfo['Website'], partyDict)
    
    dictList.append(repInfo)
  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getDELeg(partyDict)

  with open('/home/michael/Desktop/DELeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)