from lxml import html
import requests
import json


def parse_json():
    '''Picks idle packages from PortingDB and returns them as a list.'''

    with open('portingdb.json') as data_file:    
        data = json.load(data_file)
    
    packages = []

    for p in data:
        if data[p]["status"] == "idle":
            packages.append(p)

    return packages


def parse_html():
    '''Picks Python 3 compatible packages from PyPI and returns them
    as a list.'''

    page = requests.get('https://pypi.python.org/pypi?:action=browse&show=all&c=533')
    tree = html.fromstring(page.content)

    # This will create a list of packages:
    packages = tree.xpath('//tr/td/a/text()')

    # Deletes the first item, because it's not a package.
    del packages[0]

    return packages


def separate_packages_pdb():
    '''Opens the raw_portingdb.txt file with packages from portingdb
    and deletes redundant texts. It writes bare names of packages
    to portingdb.txt file.'''

    raw_portingdb = open('raw_portingdb.txt', 'r')
    portingdb = open('portingdb.txt', 'w')
    
    for line in raw_portingdb:
        splitted_line = line.split( )
        package, *_ = splitted_line
        portingdb.write(package)
        portingdb.write("\n")

    # Do not forget to close files. :)
    raw_portingdb.close()
    portingdb.close()


def separate_packages_PyPI():
    '''Opens the raw_PyPI.txt file with packages from PyPI
    and deletes redundant texts. It writes bare names of packages
    to PyPI.txt file.'''

    raw_pypi = open('raw_PyPI.txt', 'r')
    pypi = open('PyPI.txt', 'w')

    for line in raw_pypi:
        if line[0] == "<":
            splitted_line = line.split('/')
            _, _, package, _, _ = splitted_line
            pypi.write(package)
            pypi.write("\n")

    # Do not forget to close files. :)
    raw_pypi.close()
    pypi.close()

def compare_packages():
    '''Copare packages from files portingdb.txt and PyPI.txt.
    Writes packages in both files in output.txt file'''

    portingdb = open('portingdb.txt', 'r')
    output = open('output.txt', 'w')
   
    for package in portingdb:
        pypi = open('PyPI.txt', 'r')
        for py3package in pypi:
            if py3package == package:
                print("Jej! I found a Python 3 compatible package!")
                output.write(package)
#                break
#            elif limit < ord(py3package[0]):
#                break
        pypi.close()

    # Do not forget to close files. :)
    portingdb.close()
    output.close()


