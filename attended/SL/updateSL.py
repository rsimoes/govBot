from csv import DictWriter
import time, importlib, multiprocessing

data = []

def addToList(object):
  data.extend(object)
  print len(data), 'records stored'

def pullLeg(scriptList, partyDict):

  name = multiprocessing.current_process().name
  print 'Process {0} is starting on {1}'.format(name, scriptList[0])

  mod = importlib.import_module(scriptList[0])
  dictList = eval(str('mod.' + scriptList[1] + '(partyDict)'))
  print '{0} completed {1} records'.format(scriptList[0], len(dictList))
  return dictList


def parallelPull(scripts, partyDict):
  pool = multiprocessing.Pool(processes = 20)
  for script in scripts:
    pool.apply_async(pullLeg, args=(script, partyDict), callback = addToList)
  pool.close()
  pool.join()


def main():
  scripts = [['MALeg', 'getMALeg'], ['TXLeg', 'getTXLeg'], ['PALeg', 'getPALeg'], ['AKLeg', 'getAKLeg'], ['ALLeg', 'getALLeg'], ['ARLeg', 'getARLeg'], ['AZLeg', 'getAZLeg'], ['CALeg', 'getCALeg'], ['COLeg', 'getCOLeg'], ['CTLeg', 'getCTLeg'], ['DELeg', 'getDELeg'], ['FLHouse', 'getFLHouse'], ['FLSenate', 'getFLSen'], ['GAHouse', 'getGAHouse'], ['GASenate', 'getGASenate'], ['HILeg', 'getHILeg'], ['IALeg', 'getIALeg'], ['IDLeg', 'getIDLeg'], ['ILLeg', 'getILLeg'], ['INLeg', 'getINLeg'], ['KSLeg', 'getKSLeg'], ['KYLeg', 'getKYLeg'], ['LALeg', 'getLALeg'], ['MDLeg', 'getMDLeg'], ['MELeg', 'getMELeg'], ['MILeg', 'getMILeg'], ['MNHouse', 'getMNHouse'], ['MNSenate', 'getMNSenate'], ['MOLeg', 'getMOLeg'], ['MSLeg', 'getMSLeg'], ['MTLeg', 'getMTLeg'], ['NCLeg', 'getNCLeg'], ['NDLeg', 'getNDLeg'], ['NELeg', 'getNELeg'], ['NHLeg', 'getNHLeg'], ['NJLeg', 'getNJLeg'], ['NMLeg', 'getNMLeg'], ['NVLeg', 'getNVLeg'], ['NYAssembly', 'getNYAssembly'], ['NYSenate', 'getNYSenate'], ['OHLeg', 'getOHLeg'], ['OKLeg', 'getOKLeg'], ['ORLeg', 'getORLeg'], ['ORLeg', 'getORLeg('], ['RILeg', 'getRILeg'], ['SCLeg', 'getSCLeg'], ['SDLeg', 'getSDLeg'], ['TNLeg', 'getTNLeg'], ['UTLeg', 'getUTLeg'], ['VALeg', 'getVALeg'], ['VTLeg', 'getVTLeg'], ['WALeg', 'getWALeg'], ['WILeg', 'getWILeg'], ['WVLeg', 'getWVLeg'], ['WYLeg', 'getWYLeg']]
  partyDict = {'d+r': 'Unknown', 'd': 'Democratic', 'r': 'Republican', '(R)': 'Republican', '(D)': 'Democratic', '(I)':'Independent', 'R': 'Republican', 'D': 'Democratic', '': 'Unknown', 'I': 'Independent', 'Democrat': 'Democratic', 'Republican': 'Republican', 'Democratic': 'Democratic', 'Independent': 'Independent', 'U': 'Independent'}

  startTime = time.time()
  parallelPull(scripts, partyDict)
  print 'All downloaded'
  dictList = data

  with open('/home/michael/Desktop/output.csv', 'w') as output:
    dwObject = DictWriter(output, ['District', 'Name', 'Party', 'Phone', 'Address', 'Website', 'Email', 'Facebook', 'Twitter', 'Youtube', 'DOB'], restval = '')
    dwObject.writeheader()
    
    for row in dictList:
      dwObject.writerow(row)

  endTime = time.time()
  print "Completed in", endTime - startTime


if __name__ == '__main__':
  main()