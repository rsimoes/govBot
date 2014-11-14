from csv import DictWriter
from config import writePath
import requests
import json


def getNVLeg(partyDict):
    payload = {'dataType': 'json', 'house': 'Assembly'}
    url = 'http://www.leg.state.nv.us/App/Legislator/A/api/Current/Legislator'
    assemblyRequest = requests.get(url, params=payload)
    assemblyObject = json.loads(assemblyRequest.text)
    payload['house'] = 'Senate'
    senateRequest = requests.get(url, params=payload)
    senateObject = json.loads(senateRequest.text)
    dictList = []

    for item in assemblyObject:
        repInfo = {}
        if not item['IsNoLongerMember']:
            repInfo['District'] = 'NV State Assembly District {0}'.format(item['DistrictNbr'].strip())
            repInfo['Website'] = 'http://www.leg.state.nv.us/App/Legislator/A/Assembly/Current/' + item['DistrictNbr'].strip()
            if item['IsVacant']:
                repInfo['Name'] = 'VACANT'
            else:
                nameList = item['FullName'].split(',')
                name = ''
                address = ''
                if len(nameList) == 2:
                    name = nameList[1].strip() + ' ' + nameList[0].strip()
                elif len(nameList) == 3:
                    name = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
                else:
                    name = item['FullName'].strip()
                if item['Address2'] is not None:
                    address = '{0} {1} {2}, {3} {4}'.format(item['Address1'].strip(), item['Address2'].strip(), item['City'].strip(), item['State'].strip(), item['Zip'].strip()).replace('    ', ' ')
                else:
                    address = '{0} {1}, {2} {3}'.format(item['Address1'].strip(), item['City'].strip(), item['State'].strip(), item['Zip'].strip()).replace('    ', ' ')
                repInfo['Name'] = name
                repInfo['Party'] = item['Party'].strip()
                repInfo['Email'] = item['LCBEmail'].strip()
                repInfo['Address'] = address
                repInfo['Phone'] = item['LCBPhone'].strip()
            dictList.append(repInfo)

    for item in senateObject:
        repInfo = {}
        if not item['IsNoLongerMember']:
            repInfo['District'] = 'NV State Senate District {0}'.format(item['DistrictNbr'].strip())
            repInfo['Website'] = 'http://www.leg.state.nv.us/App/Legislator/A/Senate/Current/' + item['DistrictNbr'].strip()
            if item['IsVacant']:
                repInfo['Name'] = 'VACANT'
            else:
                nameList = item['FullName'].split(',')
                name = ''
                address = ''
                if len(nameList) == 2:
                    name = nameList[1].strip() + ' ' + nameList[0].strip()
                elif len(nameList) == 3:
                    name = nameList[1].strip() + ' ' + nameList[0].strip() + ' ' + nameList[2].strip()
                else:
                    name = item['FullName'].strip()
                if item['Address2'] is not None:
                    address = '{0} {1} {2}, {3} {4}'.format(item['Address1'].strip(), item['Address2'].strip(), item['City'].strip(), item['State'].strip(), item['Zip'].strip()).replace('    ', ' ')
                else:
                    address = '{0} {1}, {2} {3}'.format(item['Address1'].strip(), item['City'].strip(), item['State'].strip(), item['Zip'].strip()).replace('    ', ' ')
                repInfo['Name'] = name
                repInfo['Party'] = item['Party'].strip()
                repInfo['Email'] = item['LCBEmail'].strip()
                repInfo['Address'] = address
                repInfo['Phone'] = item['LCBPhone'].strip()
            dictList.append(repInfo)

    return dictList


if __name__ == "__main__":
    partyDict = {'D': 'Democratic', 'R': 'Republican', 'I': 'Independent', 'Republican': 'Republican', 'Democrat': 'Democratic'}
    dictList = getNVLeg(partyDict)
    with open(writePath + 'NVLeg.csv', 'w') as csvFile:
        dwObject = DictWriter(csvFile, ['District', 'Name', 'Party', 'Website', 'Phone', 'Address', 'Email', 'Facebook', 'Twitter'], restval='')
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
