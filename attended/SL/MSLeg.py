from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2


def pullIndividual(url, name, body, partyDict):
    while True:
        print url
        try:
            response = urllib2.urlopen(url)
            indivSoup = BeautifulSoup(response.read())
            indivInfo = {}
            rawDistrict = indivSoup.find('district')
            rawParty = indivSoup.find('party')
            rawEmail = indivSoup.find('email_address')
            rawPhone = indivSoup.find('cap_phone')
            rawAddress = indivSoup.find('cap_room')
            if rawDistrict is not None:
                if rawDistrict.string is not None:
                    indivInfo['District'] = 'MS State ' + body[0].upper() + body[1:] + ' District ' + rawDistrict.string.strip()
            if rawParty is not None:
                if rawParty.string is not None:
                    indivInfo['Party'] = partyDict[rawParty.string.strip()]
            if rawEmail is not None:
                if rawEmail.string is not None:
                    indivInfo['Email'] = rawEmail.string.strip() + body + '.ms.gov'
            if rawPhone is not None:
                if rawPhone.string is not None:
                    indivInfo['Phone'] = rawPhone.string.strip()
            if rawAddress is not None:
                if rawAddress.string is not None:
                    indivInfo['Address'] = 'Room ' + rawAddress.string.strip() + ' P.O. Box 1018 Jackson, MS 39215'
            indivInfo['Name'] = name.strip()
            indivInfo['Website'] = url.strip()
            return indivInfo
        except Exception:
            pass


def getMSLeg(partyDict):
    houseSoup = BeautifulSoup(urllib2.urlopen('http://billstatus.ls.state.ms.us/members/hr_membs.xml').read())
    senateSoup = BeautifulSoup(urllib2.urlopen('http://billstatus.ls.state.ms.us/members/ss_membs.xml').read())
    dictList = []
    dictList.append(pullIndividual('http://billstatus.ls.state.ms.us/members/' + houseSoup.find('chair_link').string.strip(), houseSoup.find('chair_name').string.strip(), 'house', partyDict))
    dictList.append(pullIndividual('http://billstatus.ls.state.ms.us/members/' + houseSoup.find('protemp_link').string.strip(), houseSoup.find('protemp_name').string.strip(), 'house', partyDict))
    for memberGroup in houseSoup.find_all('member'):
        for i in range(1, 6):
            dictList.append(pullIndividual('http://billstatus.ls.state.ms.us/members/' + memberGroup.find('m{0}_link'.format(i)).string.strip(), memberGroup.find('m{0}_name'.format(i)).string.strip(), 'house', partyDict))
    dictList.append(pullIndividual('http://billstatus.ls.state.ms.us/members/' + senateSoup.find('protemp_link').string.strip(), senateSoup.find('protemp_name').string.strip(), 'senate', partyDict))
    for memberGroup in senateSoup.find_all('member'):
        for i in range(1, 5):
            dictList.append(pullIndividual('http://billstatus.ls.state.ms.us/members/' + memberGroup.find('m{0}_link'.format(i)).string.strip(), memberGroup.find('m{0}_name'.format(i)).string.strip(), 'senate', partyDict))
    return dictList


if __name__ == '__main__':
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getMSLeg(partyDict)
    with open(writePath + 'MSLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
