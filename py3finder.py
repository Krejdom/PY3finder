#!/usr/bin/python3

from lxml import html
import requests
import json
import yaml
import pprint
import re
import urllib3


def parse_pypi():
    '''Picks Python 3 copmatible packages from PyPI and returns them
    as a list.'''

    page = requests.get('https://pypi.python.org/pypi?:action=browse&show=all&c=533')
    tree = html.fromstring(page.content)

    # This will create a list of packages:
    packages = tree.xpath('//tr/td/a/text()')

    # Deletes the first item, because it's not a package.
    del packages[0]

    return packages


def get_html(url):
    '''Downloads the html and convets it to the string.'''

    http = urllib3.PoolManager()
    r = http.request('GET', url)
    return r.data.decode("utf-8")


def parse_portingdb():
    '''Picks gray and red packages from PortingDB and returns them as a list.'''
    
    string = get_html('http://fedora.portingdb.xyz/')

    idle_packages = re.findall(r'DDDDDD">&nbsp;<\/span>&nbsp;<a href="\/pkg\/([\w]*-?[\w]*)\/">', string)
    blocked_pacakages = re.findall(r'D9534F">&nbsp;<\/span>&nbsp;<a href="\/pkg\/([\w]*-?[\w]*)\/">', string)

    return idle_packages + blocked_pacakages


def compare_packages(unknown, py3com):
    '''Copares packages from portingdb and PyPI.
    Writes packages from both sites into output.txt file'''

    output = open('output.txt', 'w')
    
    # Find the intersection between unknown and Python 3 compatible
    packages = sorted(set(unknown).intersection(py3com))

    cp = len(packages)
    
    # Print out the result
    if cp == 0:
        print('Nothing found.')
    elif cp == 1:
        print('I found', len(packages), 'package:', packages[0])
    else:
        print('I found', len(packages), 'packages: \n')
        for p in packages:
            print(p)

    # Write packages into the output file
    for package in packages:
        output.write(package)
        output.write("\n")

    # Do not forget to close the file. :)
    output.close()


def main():
    unknown = parse_portingdb()
    py3com = parse_pypi()
    compare_packages(unknown, py3com)


if __name__ == "__main__":
    main()
