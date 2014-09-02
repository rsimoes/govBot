import urllib2, re, xlrd
from bs4 import BeautifulSoup
from csv import DictWriter

def getCORep(url):
  while True:
    print url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    data = soup.find('table').find_all('tr')[1].find_all('td')

    phone = ''
    email = ''

    rawName = data[0].get_text().split('\n')[0].split(',')
    if len(rawName) == 2:
      name = rawName[1].strip() + ' ' + rawName[0].strip()
    elif len(rawName) == 3:
      name = rawName[2].strip() + ' ' + rawName[0].strip() + ' ' + rawName[1].strip()
    else:
      name = data[0].get_text().strip()
    name = name.replace('   ', ' ').replace('  ', ' ')
    rawContact = data[6].get_text().strip().split('\n')
    if len(rawContact) == 2:
      phone = rawContact[0][4:].strip()
      email = rawContact[1][7:].strip()
    elif len(rawContact) == 1:
      if re.search('Cap:', rawContact[0]):
        phone = rawContact[0][4:].strip()
      elif re.search('E-mail:', rawContact[0]):
        email = rawContact[0][7:].strip()
    return name, phone, email
  except Exception:
    pass

def getCOLeg(partyDict):
  for i in [1, 21, 41, 61, 81]:
    soup = BeautifulSoup(urllib2.urlopen('http://www.leg.state.co.us/clics/clics2014a/directory.nsf/Pink%20Book/l.%20All%20Legislators?OpenView&Start={0}&SimpleView=5'.format(i)).read())
    if i == 1:
      table = soup.find('table', {'cellpadding': '2'}).find_all('tr', {'valign': 'top'})
    else: table = table + soup.find('table', {'cellpadding': '2'}).find_all('tr', {'valign': 'top'})

  dictList = []

  for item in table:
    repInfo = {}
    columns = item.find_all('td')
    link = columns[0].find('a')

    repInfo['District'] = 'CO State {0} District {1}'.format(columns[1].get_text().strip(), columns[2].get_text().strip())
    repInfo['Party'] = partyDict[str(columns[3].get_text().strip())]
    repInfo['Website'] = 'http://www.leg.state.co.us' + columns[0].find('a').get('href')

    repInfo['Name'], repInfo['Phone'], repInfo['Email'] = getCORep(repInfo['Website'])

    dictList.append(repInfo)

  return dictList

if __name__ == '__main__':
  partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
  dictList = getCOLeg(partyDict)

  with open('/home/michael/Desktop/COLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)