from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import re


def getARLeg(partyDict):
    starterSoup = BeautifulSoup(urllib2.urlopen('http://www.arkleg.state.ar.us/assembly/2013/2014S2/Pages/Home.aspx'))
    url = starterSoup.find('a', {'href': re.compile('LegislatorSearchResults')}).get('href')
    soup = BeautifulSoup(urllib2.urlopen('http://www.arkleg.state.ar.us' + url).read())
    dictList = []
    for i in range(135):
        repInfo = {}
        #The row ID changes infrequently. If AR breaks, that's the first place to look
        row = soup.find('tr', {'id': 'ctl00_m_g_bcf69ea5_752a_48a4_ba1b_6d137e714e36_ctl00_gvMemberGrid_DXDataRow{0}'.format(i)})
        if row is not None:
            columns = row.find_all('td')
            link = columns[0].find('a')
            repInfo['Name'] = link.string.strip().replace('  ', ' ')
            repInfo['Website'] = link.get('href')
            if columns[1].find('a') is not None:
                repInfo['Email'] = re.sub('[Mm][Aa][Ii][Ll][Tt][Oo]:', '', columns[1].find('a').get('href'))
            repInfo['District'] = 'AR State {0} District {1}'.format(columns[2].string.strip(), columns[4].string.strip())
            if not re.search('Elect', columns[0].get_text()):
                dictList.append(repInfo)
    return dictList


if __name__ == '__main__':
    partyDict = {'(R)': 'Republican', '(D)': 'Democratic', '(I)': 'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent'}
    dictList = getARLeg(partyDict)
    with open(writePath + 'ARLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
