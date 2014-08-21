import urllib2, urllib, re, xlrd
from bs4 import BeautifulSoup
from csv import DictWriter

def getOKLeg(partyDict):
  houseSheet = xlrd.open_workbook(file_contents = urllib2.urlopen('http://www.gmodules.com/ig/proxy?url=http://www.okhouse.gov/Documents/MembersList.xls').read(), formatting_info=False).sheet_by_index(0)
  senateSheet = xlrd.open_workbook(file_contents = urllib2.urlopen('http://www.gmodules.com/ig/proxy?url=http://www.oksenate.gov/Senators/directory.xls').read(), formatting_info=False).sheet_by_index(0)
  senateSoup = BeautifulSoup(urllib2.urlopen('http://www.gmodules.com/ig/proxy?url=http://www.oksenate.gov/Senators/Default.aspx').read())
 
  dictList = []
 
  for i in range(1, 102):
    repInfo = {}
    rowValues = houseSheet.row_values(i, start_colx=0, end_colx=None)
    nameList = rowValues[0].split(',')

    if len(nameList) == 3:
      name = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
    elif len(nameList) == 2:
      name = nameList [1].strip() + ' ' + nameList[0].strip()
    else:
      name = rowValues[0]

    distNum = str(int(rowValues[2]))
    if type(rowValues[5]) is unicode:
      roomNum = str(rowValues[5])
    else:
      roomNum = str(int(rowValues[5]))
    
    repInfo['District'] = 'OK State House District ' + distNum
    repInfo['Name'] = name
    repInfo['Email'] = rowValues[1]
    repInfo['Website'] = 'http://www.okhouse.gov/District.aspx?District=' + distNum
    repInfo['Party'] = partyDict[str(rowValues[3])]
    repInfo['Phone'] = rowValues[4]
    repInfo['Address'] = '2300 N. Lincoln Blvd. Room ' + str(rowValues[5]) + ' Oklahoma City, OK 73105'
     
    dictList.append(repInfo)
  
  table = senateSoup.find('table', {'summary': "This table lists the Senators alphabetically.  Each senator's name is linked to his or her respective contact page."})
  data = table.find_all('td')

  urls = {}
  for item in data:
    link = item.find('a')
    if link is not None:
      text = item.get_text().replace('\n', ' ').strip()
      if re.search('District', text):
        distNum = str(re.sub('^.*District ([0-9]*).*$', '\\1', text))
        url = 'http://www.oksenate.gov/Senators/' + link.get('href')

        urls[distNum] = url

  for i in range(6, 54):
    repInfo = {}
    rowValues = senateSheet.row_values(i, start_colx=0, end_colx=None)
    nameList = rowValues[0].split(',')
    distNum = str(int(rowValues[3]))

    if len(nameList) == 3:
      name = nameList[2].strip() + ' ' + nameList[0].strip() + ' ' + nameList[1].strip()
    elif len(nameList) == 2:
      name = nameList [1].strip() + ' ' + nameList[0].strip()
    else:
      name = rowValues[0]

    if type(rowValues[5]) is unicode:
      roomNum = str(rowValues[5])
    else:
      roomNum = str(int(rowValues[5]))

    repInfo['District'] = 'OK State Senate District ' + distNum
    repInfo['Name'] = name
    repInfo['Party'] = partyDict[str(rowValues[1])]
    repInfo['Phone'] = '(401) 521-5'+str(int(rowValues[8]))
    repInfo['Address'] = '2300 N. Lincoln Blvd, Room Number ' + roomNum + ', Oklahoma City OK 73105'
    repInfo['Email'] = rowValues[14]
    repInfo['Website'] = urls[distNum]

    dictList.append(repInfo)
    
  return dictList
  
if __name__ == "__main__":
  partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent'}
  dictList = getOKLeg(partyDict)
  
  with open('/home/michael/Desktop/OKLeg.csv', 'w') as csvFile:
    dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Email', 'Phone', 'Address'], restval = '')
    dwObject.writeheader()

    for row in dictList:
      dwObject.writerow(row)
                                 
