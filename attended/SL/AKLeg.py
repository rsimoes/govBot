#!/usr/bin/env python

from bs4 import BeautifulSoup
from csv import DictWriter
from config import writePath
from urllib2 import urlopen
from unidecode import unidecode
import os.path
import re
import sys

sys.path.append(
    os.path.join(sys.path[0], '../../lib')
)
from govbot.util import multiline_strip

def getAKLeg():
    house, senate = map(
        lambda body: BeautifulSoup(
            urlopen('http://house.legis.state.ak.us/').read()
        ).find(
            'div', {'id': 'tab1-2'}
        ).find(
            'ul', {'class': 'people-holder'}
        ).find(
            'ul', {'class': 'item'}
        ).find_all('li'),
        ('house', 'senate')
    )

    dictList = []

    for body, table in zip(('House', 'Senate'), (house, senate)):
        for item in table:
            repInfo = {}
            repInfo['Name'] = unidecode(
                item.find('strong', {'class': 'name'}).string
            ).strip()

            link = item.find('a')
            repInfo['Website'] = link.get('href')

            dl = item.find('dl')
            district = re.search(
                r'District:\s*(\w+)', dl.get_text(), re.DOTALL
            ).group(1)
            repInfo['District'] = 'AK State {0} District {1}'.format(
                body, district
            )

            repInfo['Party'] = re.search(
            r'Party:\s*(\w+)', dl.get_text(), re.DOTALL
            ).group(1)

            repInfo['Phone'] = re.search(
                r'Phone:\s*([0-9-]+)', dl.get_text(), re.DOTALL
            ).group(1)

            repInfo['Email'] = dl.find('a').get('href').replace('mailto:', '')

            member_soup = BeautifulSoup(urlopen(repInfo['Website']).read())
            repInfo['Address'] = multiline_strip(
                re.search(
                    r'Session Contact(.+99801)',
                    member_soup.find_all('div', {'class': 'bioleft'})[1].get_text(),
                    re.DOTALL
                ).group(1)
            )
            print str(repInfo) + '\n'
            dictList.append(repInfo)

    return dictList


if __name__ == '__main__':
    dictList = getAKLeg()
    with open(os.path.join(writePath, 'AKLeg.csv'), 'w') as csvFile:
        dwObject = DictWriter(
            csvFile,
            [
                'District', 'Name', 'Party', 'Website', 'Email', 'Phone',
                'Address'
            ],
            restval='',
            lineterminator='\n'
        )
        dwObject.writeheader()
        for row in dictList:
            dwObject.writerow(row)
