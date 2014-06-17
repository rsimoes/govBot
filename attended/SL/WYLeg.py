import urllib2, urllib, re, xlrd
from bs4 import BeautifulSoup
from csv import DictWriter


def getWYLeg(partyDict):
  sheet = xlrd.open_workbook(file_contents = urllib2.urlopen('http://legisweb.state.wy.us/LegislatorSummary/App_Themes/LSO/Excel%20Contact%20Info.xls').read(), formatting_info=False).sheet_by_index(0)

  dictList = []

  for i in range(1, 91):
    repInfo = {}
    rowValues = sheet.row_values(i, start_colx=0, end_colx=None)
    distList = rowValues[0].strip().split(' ')

    repInfo['District'] = 'WY State {0} District {1}'.format(distList[0].strip(), int(distList[2].strip()))
    repInfo['Name'] = rowValues[1].strip() + ' ' + rowValues[2].strip()
    repInfo['Party'] = partyDict[str(rowValues[3].strip())]
    repInfo['Address'] = '{0} {1}, {2} {3}'.format(rowValues[4].strip(), rowValues[5].strip(), rowValues[6].strip(), str(rowValues[7]).strip())
    repInfo['Phone'] = rowValues[8].strip()
    repInfo['Email'] = rowValues[11].strip()

    dictList.append(repInfo)

  return dictList

  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent', 'Republican': 'Republican', 'Democrat': 'Democratic'}
  dictList = getWYLeg(partyDict)
  
  with open('/home/michael/Desktop/WYLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)