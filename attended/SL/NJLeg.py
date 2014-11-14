from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import urllib
import re


def getRep(url):
    while True:
        try:
            print url
            response = urllib2.urlopen(url, timeout=5)
            indiesoup = BeautifulSoup(response.read())
            table = indiesoup.find_all('tr')
            DOB = ''
            Address = ''
            Phone = ''
            for item in table:
                text = item.get_text()
                if text is not None:
                    if re.search('BORN:', text):
                        DOB = text.replace('BORN:', '').strip()
                    if re.search('DISTRICT OFFICE ADDRESS:', text):
                        Address = text.replace('DISTRICT OFFICE ADDRESS:', '').strip().replace('\n', ' ').replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
                    if re.search('PHONE NUMBER:', text):
                        Phone = text.replace('PHONE NUMBER:', '').strip()
            return DOB, Address, Phone
        except Exception:
            pass


def getNJLeg(unnecessaryArg):
    url = 'http://www.njleg.state.nj.us/members/roster.asp'
    dictList = []
    for i in range(1, 41):
        data = urllib.urlencode({'District': str(i)})
        html = urllib2.urlopen(url, data).read()
        soup = BeautifulSoup(html)
        chambers = ['Senate', 'Assembly', 'Assembly']
        links = soup.find_all('a', {'href': re.compile('BIO.asp')})
        for j in range(3):
            repInfo = {}
            link = links[j]
            repInfo['District'] = 'NJ State ' + chambers[j] + ' District ' + str(i)
            repInfo['Name'] = link.string.strip().replace(u"\u00A0", ' ').title().replace('  ', ' ')
            repInfo['Website'] = 'http://www.njleg.state.nj.us/members/' + link.get('href')
            contactInfo = getRep(repInfo['Website'])
            if contactInfo is not None:
                repInfo['DOB'], repInfo['Address'], repInfo['Phone'] = getRep(repInfo['Website'])
            dictList.append(repInfo)
    return dictList


if __name__ == "__main__":
    dictList = getNJLeg('')
    with open(writePath + 'NJLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Website', 'DOB', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
