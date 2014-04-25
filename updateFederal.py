from bs4 import BeautifulSoup
import urllib2, csv, re

senateURL = 'http://www.senate.gov/general/contact_information/senators_cfm.xml'
houseURL = 'http://clerk.house.gov/member_info/text-labels-113.txt'
partyDict = {'R': 'Republican', 'D': 'Democratic', 'I': 'Independent','': 'Unknown'}
nextElection = '2014-11-04'
nextInauguration = '2015-01-03'

def downloadSenate(url):
  response = urllib2.urlopen(url)
  if response.code != 200:
    raise exception('Not connecting to Senate')
  else:
    xml = response.read()
    page = BeautifulSoup(xml)
    names = []
    parties = {}
    states = {}
    addresses = {}
    websites = {}
    
    for member in page.find_all('member'):
      if re.search(',', member.first_name.string):
        first, suffix = member.first_name.string.split(',')
      else:
        first = member.first_name.string
        suffix = ''
      name = first + ' ' + member.last_name.string + ' ' + suffix
      name = name.replace("   ", " ").replace("  ", " ").decode("Windows-1252").replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      name = re.sub(' $','',name)
      name = unicode(name)
      party = partyDict[member.party.string]
      state = member.state.string
      address = member.address.string
      website = member.website.string
    
      names.append(name)
      parties[name] = party
      states[name] = state
      addresses[name] = address
      websites[name] = website
    return [names, parties, states, addresses, websites]

def downloadHouse(url):
  response = urllib2.urlopen(url)
  if response.code != 200:
    raise exception('Not connecting to House')
  else:
    drObject = csv.DictReader(response, delimiter='\t')
    districts = [] 
    names = {}
    parties = {}
    addresses = {}
    for member in drObject:
      name = member['FirstName'] + ' ' + member['MiddleName'] + ' ' + member['LastName'] + ' ' + member['Suffix']
      name = name.replace("   ", " ").replace("  ", " ").decode("Windows-1252").replace(u'\u2018',"'").replace(u'\u2019',"'").replace(u'\u201A',"'").replace(u'\u201B',"'").replace(u'\u2039',"'").replace(u'\u203A',"'").replace(u'\u201C','"').replace(u'\u201D','"').replace(u'\u201E','"').replace(u'\u201F','"').replace(u'\u00AB','"').replace(u'\u00BB','"').replace(u'\u00e0','a').replace(u'\u00e1','a').replace(u'\u00e8','e').replace(u'\u00e9','e').replace(u'\u00ec','i').replace(u'\u00ed','i').replace(u'\u00f2','o').replace(u'\u00f3','o').replace(u'\u00f9','u').replace(u'\u00fa','u')
      name = re.sub(" $", "", name)
      name = unicode(name)
      district = member['113 St/Dis']
      party = partyDict[member['Party']] 
      address = member['Address'] + ' ' + member['City'] + ', ' + member['State'] + ' ' + member['Zip+4']
      
      districts.append(district)
      names[district] = name
      parties[district] = party
      addresses[district] = address
    return [districts, names, parties, addresses]

def verifyCSV(filename, senateObject, houseObject):
  senateNames, senateParties, senateStates, senateAddresses, senateWebsites = senateObject
  houseDistricts, houseNames, houseParties, houseAddresses = houseObject
  congress = []
  notinSenate = []
  notinHouse = {}
  notinSenateCSV = senateNames 
  notinHouseCSV = houseDistricts
  knownReps = []
  allegedHouseNames = {}
  unknowns = {}
  
  with open(filename,'r') as federalFile:
    drObject = csv.DictReader(federalFile)
    count = 0
    for congressperson in drObject:
      congress.append(congressperson)
      count += 1
    print count, 'Representatives'
  for congressperson in congress:
    if congressperson['Body Name'] == 'US Senate':
      if congressperson['Official Name'] in senateNames:
        notinSenateCSV.remove(congressperson['Official Name'])
        knownReps.append(congressperson)
      else:
        notinSenate.append(congressperson)
    elif congressperson['Body Name'] == 'US House of Representatives':
      rawDist = congressperson['Electoral District']
      if len(rawDist) == 2:
        electoralDist = rawDist + '00'
      else:
        electoralDist = congressperson['Body Represents - State'] + rawDist[len(rawDist)-2:].replace(" ","0")
      allegedHouseNames[electoralDist] = congressperson['Official Name']
      if houseNames[electoralDist] == congressperson['Official Name']: 
        notinHouseCSV.remove(electoralDist)
        knownReps.append(congressperson)
      else:
        notinHouse[electoralDist] = congressperson
    else:
      print 'Skipping', congressperson['Office Name'], congressperson['Official Name']
      knownReps.append(congressperson)
  print len(knownReps), 'known Representatives'
  print len(notinHouse), 'incorrect House names'
  print len(notinHouseCSV), 'missing Representatives'
  print len(notinSenate), 'incorrect Senate names'
  print len(notinSenateCSV), 'missing Senators'
  return [notinHouse, notinSenate, notinHouseCSV, notinSenateCSV, allegedHouseNames, knownReps, unknowns]

def promptAndChange(outputDir, errors, houseObject, senateObject):
  notinHouse, notinSenate, notinHouseCSV, notinSenateCSV, allegedHouseNames, knownReps, congress = errors
  senateNames, senateParties, senateStates, senateAddresses, senateWebsites = senateObject
  houseDistricts, houseNames, houseParties, houseAddresses = houseObject
  
  for nonrep in notinHouse:
    oldInfo = notinHouse[nonrep]
    nameDict = {'C':allegedHouseNames[nonrep], 'W':houseNames[nonrep]}
    print 'for', nonrep,' CSV shows',nameDict['C']
    print 'for', nonrep,' Website shows', nameDict['W']
    newNameStatus = str(raw_input('Is this a new representative? (Y/N):')).upper()
    
    while newNameStatus not in ['Y','N']:
      newNameStatus = str(raw_input('Please select from new (Y) or not new (N):')).upper()
    
    if newNameStatus == 'N':
      repInfo = oldInfo
      useNameFrom = str(raw_input('Use name from (C)SV or (W)ebsite:')).upper()
      
      while useNameFrom not in ['W', 'C']:
        useNameFrom = str(raw_input('Please choose from (C)SV or (W)ebsite:')).upper()
      
      repInfo['Official Name'] = nameDict[useNameFrom]
      knownReps.append(repInfo)
    
    else:
      newDOB = str(raw_input("Enter their DOB (yyyy-mm-dd):"))
      newWebsite = str(raw_input("Enter their website:"))
      newPhone = str(raw_input("Enter their phone:"))
      newYoutube = str(raw_input("Enter their YouTube:"))
      newFacebook = str(raw_input("Enter their Facebook:"))
      newTwitter = str(raw_input("Enter their Twitter:"))
      newWiki = str(raw_input("Enter their WikiWord:"))
      newGoog = str(raw_input("Enter their Google+:"))

      repInfo = {'Body Represents - County': '', 
                 'DOB': newDOB, 
                 'Next Election': nextElection, 
                 'State': nonrep[:2], 
                 'Election Month': nextElection[5:7], 
                 'Completed?': 'TRUE', 
                 'Email': '', 
                 'Website': newWebsite, 
                 'UID': 'FEe00475', 
                 'OCDID': '', 
                 'Election Year': '2014', 
                 'Expires': nextInauguration, 
                 'Phone': newPhone, 
                 'Birth Day': newDOB[8:], 
                 'Body Name': 'US House of Representatives', 
                 'Office Name': 'United State House of Representatives WI-08', 
                 'Youtube': newYoutube, 
                 'Office Level': 'Federal - Lower', 
                 'Electoral District': 'WI Congressional District 8', 
                 'Birth Year': newDOB[:4], 
                 'Body Represents - State': nonrep[:2], 
                 'Election Day': nextElection[8:], 
                 'Body Represents - Muni': '', 
                 'Expires Month': nextInauguration[5:7], 
                 'Wiki Word': newWiki, 
                 'Google Plus URL': newGoog, 
                 'Mailing Address': houseAddresses[nonrep], 
                 'Source': 'http://www.house.gov/representatives/', 
                 'Official Name': nameDict['W'], 
                 'Official Party': houseParties[nonrep], 
                 'Expires Year': newInauguration[:4], 
                 'Birth Month': newDOB[5:7], 
                 'Expires Day': newInauguration[8:], 
                 'Facebook URL': newFacebook, 
                 'Twitter Name': newTwitter
      } 
      knownReps.append(repInfo)

  ##Add in senate later

  print len(knownReps), 'known Representatives'
  saveBool = str(raw_input("Save File? (Y/N):")).upper()
  while saveBool not in ['Y', 'N']:
    saveBool = str(raw_input("No really, choose Y or N")).upper()
  if saveBool == 'Y':
    fields = [ 'UID', 'State', 'Office Level', 'Body Name', 'Body Represents - State', 'Body Represents - County', 'Body Represents - Muni', 'Electoral District', 'Office Name', 'Official Name', 'Official Party', 'Completed?', 'Phone', 'Mailing Address', 'Website', 'Email', 'Facebook URL', 'Twitter Name', 'Google Plus URL', 'Wiki Word', 'Youtube', 'Birth Year', 'Birth Month', 'Birth Day', 'DOB', 'Election Year', 'Election Month', 'Election Day', 'Next Election', 'Expires Year', 'Expires Month', 'Expires Day', 'Expires', 'Source', 'OCDID', 'Zip']
    with open(outputDir, 'w') as output:
      dwObject = csv.DictWriter(output, fields, restval = '', delimiter = ',')
      dwObject.writeheader()
      for row in knownReps:
        dwObject.writerow(row)
   
if __name__ == '__main__':
  senateObject = downloadSenate(senateURL)
  houseObject = downloadHouse(houseURL)
  errors = verifyCSV('/home/michael/Dropbox (NOIEF)/noBIP/social_media_collection/office_holders/FE Office Holders.csv', senateObject, houseObject)
  promptAndChange('/home/michael/Desktop/test.csv',errors, houseObject, senateObject) 

