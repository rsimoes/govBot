from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getContact(url):
    print url
    contactSoup = BeautifulSoup(urllib2.urlopen(url).read())
    address = ''
    phone = ''
    email = ''
    analog = contactSoup.find_all('div', {'class': 'adr'})
    for item in analog:
        namespan = item.find('span', {'class': 'fn'})
        if namespan is not None:
            if item.find('span', {'class': 'fn'}).get_text().strip() == 'Albany Office':
                street = item.find(re.compile('(span)|(div)'), {'class': 'street-address'}).get_text().replace('\n', '').strip().replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
                city = item.find(re.compile('(span)|(div)'), {'class': 'locality'}).string.strip()
                state = item.find(re.compile('(span)|(div)'), {'class': 'region'}).string.strip()
                zip5 = item.find(re.compile('(span)|(div)'), {'class': 'postal-code'}).string.strip()
                address = street + ' ' + city + ', ' + state + ' ' + zip5
                rawphone = item.find('div', {'class': 'tel'})
                rawemail = contactSoup.find('span', {'class': 'spamspan'})
                if rawphone is not None:
                    phone = rawphone.find('span', {'class': 'value'}).string.strip()
                if rawemail is not None:
                    username = rawemail.find('span', {'class': 'u'}).string.strip()
                    domain = re.sub(' \[dot\] ', '.', rawemail.find('span', {'class': 'd'}).string.strip())
                    email = username + '@' + domain
                return phone, address, email


def getNYSenate(partyDict):
    dictList = []
    soup = BeautifulSoup(urllib2.urlopen('http://www.nysenate.gov/senators'))
    table = soup.find_all('div', {'class': re.compile('views-row')})
    for item in table:
        repInfo = {}
        identInfo = item.find('div', {'class': 'views-field-field-last-name-value'})
        distInfo = item.find('div', {'class': 'views-field-field-senators-district-nid'})
        rawdist = re.sub('<.*$', '', re.sub('^<.*?>', '', str(distInfo.find('span', {'class': 'field-content'}))))
        nameList = identInfo.find('a').string.strip().split(', ')
        if len(nameList) == 3:
            repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
        elif len(nameList) == 2:
            repInfo['Name'] = nameList[1].strip() + ' ' + nameList[0].strip()
        else:
            repInfo['Name'] = nameList[0].strip()
        repInfo['Name'] = repInfo['Name'].replace("   ", " ").replace("  ", " ").replace(u'\u2018', "'").replace(u'\u2019', "'").replace(u'\u201A', "'").replace(u'\u201B', "'").replace(u'\u2039', "'").replace(u'\u203A', "'").replace(u'\u201C', '"').replace(u'\u201D', '"').replace(u'\u201E', '"').replace(u'\u201F', '"').replace(u'\u00AB', '"').replace(u'\u00BB', '"').replace(u'\u00e0', 'a').replace(u'\u00e1', 'a').replace(u'\u00e8', 'e').replace(u'\u00e9', 'e').replace(u'\u00ec', 'i').replace(u'\u00ed', 'i').replace(u'\u00f2', 'o').replace(u'\u00f3', 'o').replace(u'\u00f9', 'u').replace(u'\u00fa', 'u')
        repInfo['Website'] = 'http://www.nysenate.gov' + identInfo.find('a').get('href')
        repInfo['District'] = 'NY State Senate ' + rawdist

        contactpage = 'http://www.nysenate.gov' + item.find('span', {'class': 'contact'}).find('a').get('href')
        result = getContact(contactpage)
        if result is not None:
            repInfo['Phone'], repInfo['Address'], repInfo['Email'] = result

        rawfacebook = item.find('a', {'class': 'facebook'})
        rawtwitter = item.find('a', {'class': 'twitter'})
        rawyoutube = item.find('a', {'class': 'youtube'})
        if rawfacebook is not None:
            repInfo['Facebook'] = rawfacebook.get('href')
        if rawtwitter is not None:
            repInfo['Twitter'] = re.sub('^.*/', '', rawtwitter.get('href'))
        if rawyoutube is not None:
            repInfo['Youtube'] = re.sub('^.*/', '', rawyoutube.get('href'))
        dictList.append(repInfo)
    return dictList


if __name__ == '__main__':
    partyDict = {'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent', 'DFL': 'Democratic-Farmer Labor'}
    dictList = getNYSenate(partyDict)
    with open(writePath + 'NYSenate.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Website', 'Party', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter', 'Youtube'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
