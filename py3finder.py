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

    return idle_packages, blocked_pacakages


def write_in_file(b_packages, i_packages):
    '''
    '''

    output = open('output.txt', 'w')

    # Write idle packages into the output file
    output.write('IDLE PACKAGES:\n')
    for package in i_packages:
        output.write(package)
        output.write("\n")

    output.write("\n")

    # Write blocked packages into the output file
    output.write('BLOCKED PACKAGES:\n')
    for package in b_packages:
        output.write(package)
        output.write("\n")

    # Do not forget to close the file. :)
    output.close()


def print_result(typ, packages):

    # Print out the result
    print(typ, 'PACKAGES ({})'.format(len(packages)))
    for p in packages:
        print(p)
    print()

def compare_packages(unknown, py3com):
    '''Copares packages from portingdb and PyPI.
    Writes packages from both sites into output.txt file'''

    idle, blocked = unknown

    # Find the intersection between unknown and Python 3 compatible
    i_packages = sorted(set(idle).intersection(py3com))
    b_packages = sorted(set(blocked).intersection(py3com))
    
    print_result('IDLE', i_packages)
    print_result('BLOCKED', b_packages)

    write_in_file(b_packages, i_packages)


def main():
    compare_packages(parse_portingdb(), parse_pypi())


if __name__ == "__main__":
    main()
