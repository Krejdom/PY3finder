from lxml import html
import requests
import json


def parse_portingdb():
    '''Picks idle packages from PortingDB and returns them as a list.'''
    
    # TODO: get data from this ulr directly in this function
    # https://raw.githubusercontent.com/fedora-python/portingdb/532958f193bcaec12dc97808ec5011de90096c64/data/loc.json
    with open('portingdb.json') as data_file:    
        data = json.load(data_file)
    
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
   
    for package in portingdb:
        for py3package in pypi:
            if py3package == package:
                print("Hurray! I found a Python 3 compatible package! -", package)
                #TODO: write each package on the new line
                output.write(package)

    # Do not forget to close the file. :)
    output.close()

compare_packages()

