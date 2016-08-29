#!/usr/bin/python3

from lxml import html
import requests
import json
import yaml
import pprint


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


def list_dropped(url):
    '''Picks packages with status 'dropped' in PortingDB and returns them
    as a list.'''
    # https://raw.githubusercontent.com/fedora-python/portingdb/570702f44b4e6b2f90788176d5374878d70d8eb3/data/fedora-update.yaml
    # https://raw.githubusercontent.com/fedora-python/portingdb/master/data/upstream.yaml
    
    page = requests.get(url)
    data = page.text
    yaml_data = yaml.load(data)

    # Create a list of all names of packages
    packages = yaml_data.keys()
    
    # Initialize the list for dropped packages    
    dropped_packages = []

    # Iterate over packages and pick ones with dropped status.
    for package in packages:
        # Some packages has not a 'status', it raises a Key Error
        if 'status' in yaml_data[package].keys():
            if yaml_data[package]['status'] == 'dropped':
                dropped_packages.append(package)
    
    return dropped_packages


def compare_packages(idle, py3com, dropped):
    '''Copares packages from portingdb and PyPI.
    Writes packages from both sites into output.txt file'''

    output = open('output.txt', 'w')
    
    # Find the match
    packages = set(idle).intersection(py3com)
    packages = set(packages).difference(dropped)

    packages = sorted(packages)
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
    idle = parse_portingdb()
    py3com = parse_pypi()
    dropped = list_dropped('https://raw.githubusercontent.com/fedora-python/portingdb/570702f44b4e6b2f90788176d5374878d70d8eb3/data/fedora-update.yaml') + list_dropped('https://raw.githubusercontent.com/fedora-python/portingdb/master/data/upstream.yaml')
    compare_packages(idle, py3com, dropped)


if __name__ == "__main__":
    main()
