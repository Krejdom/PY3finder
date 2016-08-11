from lxml import html
import requests
import json


def parse_portingdb():
    '''Picks idle packages from PortingDB and returns them as a list.'''
    
    page = requests.get('https://raw.githubusercontent.com/fedora-python/portingdb/master/data/fedora.json')
    data = page.json()
    
    packages = []

    for p in data:
        if data[p]["status"] == "idle":
            packages.append(p)

    return packages


def parse_pypi():
    '''Picks Python 3 compatible packages from PyPI and returns them
    as a list.'''

    page = requests.get('https://pypi.python.org/pypi?:action=browse&show=all&c=533')
    tree = html.fromstring(page.content)

    # This will create a list of packages:
    packages = tree.xpath('//tr/td/a/text()')

    # Deletes the first item, because it's not a package.
    del packages[0]

    return packages


def compare_packages():
    '''Copares packages from portingdb and PyPI.
    Writes packages from both sites into output.txt file'''

    portingdb = parse_portingdb()
    pypi = parse_pypi()
    output = open('output.txt', 'w')
    
    # find the match
    packages = set(portingdb).intersection(pypi)
    cp = len(packages)
    
    # print out the result
    if cp == 0:
        print('Nothing found.')
    elif cp == 1:
        print('I found', len(packages), 'package:', packages[0])
    else:
        print('I found', len(packages), 'packages: \n')
        for p in packages:
            print(p)

    # write packages into the output file
    for package in packages:
        output.write(package)
        output.write("\n")

    # Do not forget to close the file. :)
    output.close()

compare_packages()

