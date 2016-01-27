#!/usr/bin/env python

from bs4 import BeautifulSoup
from config import writePath
from unidecode import unidecode
from urllib2 import urlopen
import csv
import os.path
import re
import sys

sys.path.append(
    os.path.join(sys.path[0], '../../lib')
)
from govbot.util import multiline_strip

def get_tx_rep(url, body):

    print 'Fetching ' + url + ' ...'

    # In case of connection failure:
    while True:
        try:
            response = urlopen(url)
            break
        except:
            continue

    soup = BeautifulSoup(response.read(), 'lxml')

    return {
        'house':  get_house_rep,
        'senate': get_senator
    }[body](soup)


# Strip HTML tags, leading and trailing spaces on each line, redundant spacing:
def multiline_strip(string):
    string = re.sub(r'\<.+?>', '', string)
    string = re.sub(r'[ \t]+', ' ', string)
    string = re.sub(r'^\s+|\s+$', '', string, flags=re.MULTILINE)
    string = re.sub('[\n\r]+', '\n', string)
    return string


def get_house_rep(soup):
    member_info = soup.find('div', {'class': 'member-info'})

    number = re.search(
        r'District (\d+)', str(member_info)
    ).group(1)
    district = 'TX State House District %s' % number

    # TX House member names are in "Last, First" format:
    def rewrite_name(string):
        search = re.search('Rep. (.+?)(?:, (?!Jr.))(.+)', string)
        if search is None:
            return None

        first, last = search.group(2).strip(), search.group(1).strip()
        return unidecode(first + ' ' + last).strip()

    name = rewrite_name(member_info.find('h2').get_text())

    phone = re.search(
        r'\([0-9]{3}\)\s[0-9]{3}-[0-9]{4}',
        str(member_info)
    ).group()

    address = multiline_strip(
        re.search(
            r'Capitol Address:(.+?787\d{2})',
            str(member_info),
            re.DOTALL
        ).group(1)
    )

    return {
        'District': district,
        'Name':     name,
        'Phone':    phone,
        'Address':  address
    }


def get_senator(soup):
    memtitle = soup.find('div', {'class': 'memtitle'})

    number = re.search(r'District (\d+)', memtitle.string).group(1)
    district = 'TX State Senate District %s' % number

    name = unidecode(
        re.search(r'Senator (.+):', memtitle.string).group(1).strip()
    )

    memoffice = re.sub(
        r'<.+?>',
        '\n',
        str(soup.find('td', {'class': 'memoffice'}))
    ).strip()

    search = re.search(
        r'(The Honorable.+787\d{2}).*(\(\d{3}\).+\d{3}-\d{4})',
        memoffice,
        re.DOTALL
    )

    address = thorough_strip(search.group(1))

    phone = search.group(2).strip()

    return {
        'District': district,
        'Name':     name,
        'Phone':    phone,
        'Address':  address
    }


# Start with the state-provided directories of members and then go to each
# member's page:
def get_tx_leg():

    base_urls = {
        'house':  'http://www.house.state.tx.us',
        'senate': 'http://www.senate.state.tx.us/75r/Senate/'
    }
    tables = {
        'house': BeautifulSoup(
            urlopen('http://www.house.state.tx.us/members').read(),
            'lxml'
        ).find(
            'table', {'cellspacing': '10'}
        ).find_all('td'),

        'senate': BeautifulSoup(
            urlopen(
                'http://www.senate.state.tx.us/75r/Senate/Members.htm'
            ).read(),
            'lxml'
        ).find(
            'table', {'summary': '3 column layout of List of senators by name'}
        ).find_all('li')
    }

    dict_list = []

    for body in ('house', 'senate'):
        for item in tables[body]:
            rep_info = {}
            link = item.find('a')

            if link is None:
                continue

            url = base_urls[body] + link.get('href')
            rep_info = {'Website': url}
            rep_info.update(get_tx_rep(url, body))

            # Skip entries with None values:
            if len(filter(lambda val: val is None, rep_info.values())) > 0:
                continue

            print str(rep_info) + '\n'

            dict_list.append(rep_info)

    return dict_list


if __name__ == '__main__':
    dict_list = get_tx_leg()
    with open(os.path.join(writePath, 'TXLeg.csv'), 'w') as csv_file:
        csv = csv.DictWriter(
            csv_file,
            [
                'District', 'Name', 'Party', 'Website', 'Phone', 'Address',
                'Email', 'Facebook', 'Twitter'
            ],
            restval='',
            lineterminator='\n'
        )
        csv.writeheader()
        for row in dict_list:
            csv.writerow(row)
