from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
import urllib2
import xlrd
import re


def getMERep(url):
    print url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    email = ''
    emailLink = soup.find('a', {'href': re.compile('[Mm][Aa][Ii][Ll][Tt][Oo]:')})
    if emailLink is not None:
        email = re.sub(r'^.*[Mm][Aa][Ii][Ll][Tt][Oo]:(.*)$', r'\1', emailLink.get('href'))
    return email


def getMELeg(partyDict):
    senateDownloadURL = BeautifulSoup(urllib2.urlopen('http://legisweb1.mainelegislature.org/wp/senate/downloadable-documents/').read(), 'lxml').find('a', {'href': re.compile('\.xlsx')}).get('href')
    houseSoup = BeautifulSoup(urllib2.urlopen('http://www.maine.gov/legis/house/dist_mem.htm').read())
    senateSheet = xlrd.open_workbook(file_contents=urllib2.urlopen(senateDownloadURL).read(), formatting_info=False).sheet_by_index(0)
    houseTable = houseSoup.find_all('p')
    dictList = []

    for item in houseTable:
        repInfo = {}
        link = item.find('a', {'href': re.compile('hsebios')})
        if link is not None:
            text = item.get_text().split(' - ')
            repInfo['District'] = 'ME State House {0}'.format(text[0].strip())
            repInfo['Website'] = 'http://www.maine.gov/legis/house/' + link.get('href')
            name = text[1].replace('Representative', '').strip().split(' (')
            repInfo['Name'] = name[0].strip()
            if len(name) > 1:
                repInfo['Party'] = partyDict[str(name[1][:1])]
            repInfo['Email'] = getMERep(repInfo['Website'])
            dictList.append(repInfo)

    for i in range(1, 36):
        repInfo = {}
        rowValues = senateSheet.row_values(i, start_colx=0, end_colx=None)
        repInfo['District'] = 'ME State Senate District {0}'.format(int(rowValues[1]))
        repInfo['Name'] = '{0} {1} {2}'.format(rowValues[2].strip(), rowValues[3].strip(), rowValues[4].strip()).replace('  ', ' ')
        repInfo['Party'] = partyDict[str(rowValues[6].strip())]
        repInfo['Address'] = '{0} {1}, ME {2}'.format(rowValues[7].strip(), rowValues[8].strip(), rowValues[10].strip())
        repInfo['Email'] = rowValues[11].strip()
        repInfo['Phone'] = rowValues[14].strip()
        dictList.append(repInfo)

    return dictList


if __name__ == "__main__":
    partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent', 'U': 'Unenrolled'}
    dictList = getMELeg(partyDict)
    with open(writePath + 'MELeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
