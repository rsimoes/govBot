from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getHILeg(partyDict):
    while True:
        try:
            response = urllib2.urlopen('http://www.capitol.hawaii.gov/members/legislators.aspx?chamber=all')
            if response.code == 200:
                break
        except Exception as error:
            print type(error)
            print error
            pass
    html = response.read()
    soup = BeautifulSoup(html, 'html5lib')
    bodyDict = {'H': 'House', 'S': 'Senate'}
    dictList = []

    for i in range(2, 78):
        repInfo = {}
        mainLink = soup.find('a', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_HyperLinkLast'.format(i)})
        rawFirst = soup.find('span', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_LabelFirst'.format(i)})
        rawSur = soup.find('span', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_LabelSur'.format(i)})
        rawParty = soup.find('span', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_LabelParty'.format(i)})
        rawRoom = soup.find('span', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_LabelRoom2'.format(i)})
        rawPhone = soup.find('span', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_LabelPhone2'.format(i)})
        rawEmail = soup.find('', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_HyperLinkEmail'.format(i)})
        rawFacebook = soup.find('a', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_HyperLinkFacebook'.format(i)})
        rawTwitter = soup.find('a', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_HyperLinkTwitter'.format(i)})
        rawYoutube = soup.find('a', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_HyperLinkYouTube'.format(i)})
        rawBody = soup.find('span', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_LabelDis'.format(i)})
        rawDistrict = soup.find('span', {'id': 'ctl00_ContentPlaceHolderCol1_GridView1_ctl{:02}_LabelDistrict'.format(i)})

        if rawDistrict is not None and rawBody is not None:
            repInfo['District'] = 'HI State {0} District {1}'.format(bodyDict[str(rawBody.string.strip()).upper()], rawDistrict.string.strip())
        else:
            repInfo['District'] = ''
        if mainLink.string is not None:
            last = mainLink.string.strip()
            repInfo['Website'] = 'http://www.capitol.hawaii.gov/' + mainLink.get('href')
        else:
            last = ''
            repInfo['Website'] = ''
        if rawFirst.string is not None:
            first = rawFirst.string.strip()
        else:
            first = ''
        if rawSur.string is not None:
            sur = rawSur.string.strip()
        else:
            sur = ''

        repInfo['Name'] = '{0} {1} {2}'.format(first, last, sur).replace('  ', ' ').strip()

        if rawRoom.string is not None:
            repInfo['Address'] = 'Room {0} 415 South Beretania St Honolulu, HI 96813'.format(rawRoom.string.strip())
        else:
            repInfo['Address'] = ''
        if rawParty.string is not None:
            repInfo['Party'] = partyDict[rawParty.string.strip()]
        else:
            repInfo['Party'] = partyDict['']
        if rawPhone.string is not None:
            repInfo['Phone'] = rawPhone.string.strip()
        else:
            repInfo['Phone'] = ''
        if rawEmail.string is not None:
            repInfo['Email'] = rawEmail.string.strip()
        else:
            repInfo['Email'] = ''
        if rawFacebook is not None:
            repInfo['Facebook'] = re.sub('^.*page=', '', rawFacebook.get('href'))
        else:
            repInfo['Facebook'] = ''
        if rawTwitter is not None:
            repInfo['Twitter'] = re.sub('^.*/', '', rawTwitter.get('href'))
        else:
            repInfo['Twitter'] = ''
        if rawYoutube is not None:
            repInfo['Youtube'] = re.sub('(^.*channel/)|(\\?.*$)', '', rawYoutube.get('href'))
        else:
            repInfo['Youtube'] = ''

        dictList.append(repInfo)

    return dictList

if __name__ == '__main__':
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getHILeg(partyDict)
    with open(writePath + 'HILeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Phone', 'Address', 'Website', 'Email', 'Facebook', 'Twitter', 'Youtube'])
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
