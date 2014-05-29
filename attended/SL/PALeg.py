import urllib2, urllib, re
from bs4 import BeautifulSoup
from csv import DictWriter

def repDownload(url):
  print url
  soup = BeautifulSoup(urllib2.urlopen(url).read())
  social = soup.find('div', {'class': 'Widget MemberBio-SocialLinks'})
  
  facebook = ''
  twitter = ''
  email = ''
  phone = ''
  address = ''

  rawfacebook = social.find('a', {'href': re.compile('facebook')})
  rawtwitter = social.find('a', {'href': re.compile('twitter')})

  ##finish these later
#  rawemail = 
#  rawphone = 

  rawaddress = str(soup.find('address')).split('<br/>')
  
  if rawfacebook is not None:
    facebook = rawfacebook.get('href')
  if rawtwitter is not None:
    twitter = re.sub(r'^.*/(.*)$', r'\1', rawtwitter.get('href'))
  
  address = rawaddress[1].strip() + ' ' + rawaddress[2].strip()

  return facebook, twitter, email, phone, address

def getPALeg(partyDict):
  houseSoup = BeautifulSoup(urllib2.urlopen('http://www.legis.state.pa.us/cfdocs/legis/home/member_information/mbrList.cfm?body=H&sort=district').read())
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.legis.state.pa.us/cfdocs/legis/home/member_information/mbrList.cfm?body=S&sort=district').read())
  
  houseTable = houseSoup.find('div', {'class': 'MemberInfoList-ListContainer clearfix'}).find_all('div', {'class': 'MemberInfoList-MemberBio'})
  senateTable = senateSoup.find('div', {'class': 'MemberInfoList-ListContainer clearfix'}).find_all('div', {'class': 'MemberInfoList-MemberBio'})

  dictList = []

  for item in houseTable:
    repInfo = {}

    link = item.find('a')
    nameList = link.string.split(',')

    if len(nameList) > 2:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
    elif len(nameList) == 2:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
    else:
      repInfo['Name'] = link.string.strip()

    repInfo['Website'] = 'http://www.legis.state.pa.us/cfdocs/legis/home/member_information/' + link.get('href')
    repInfo['District'] = 'PA State House ' + item.get_text().split('\n')[3].strip()
    repInfo['Party'] = partyDict[str(re.sub(r'^.*\((.)\).*$', r'\1', item.get_text().replace('\n', '').strip()))]

    repInfo['Facebook'], repInfo['Twitter'], repInfo['Email'], repInfo['Phone'], repInfo['Address'] = repDownload(repInfo['Website'])

    dictList.append(repInfo)

  for item in senateTable:
    repInfo = {}

    link = item.find('a')
    nameList = link.string.split(',')

    if len(nameList) > 2:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
    elif len(nameList) == 2:
      repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
    else:
      repInfo['Name'] = link.string.strip()

    repInfo['Website'] = 'http://www.legis.state.pa.us/cfdocs/legis/home/member_information/' + link.get('href')
    repInfo['District'] = 'PA State Senate ' + item.get_text().split('\n')[3].strip()
    repInfo['Party'] = partyDict[str(re.sub(r'^.*\((.)\).*$', r'\1', item.get_text().replace('\n', '').strip()))]

    repInfo['Facebook'], repInfo['Twitter'], repInfo['Email'], repInfo['Phone'], repInfo['Address'] = repDownload(repInfo['Website'])

    dictList.append(repInfo)

    
  return dictList
  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
  dictList = getPALeg(partyDict)
  
  with open('/home/michael/Desktop/PALeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)
                                 
