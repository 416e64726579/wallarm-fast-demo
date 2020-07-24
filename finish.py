#!/usr/bin/env python3

import sys
import re
import os
import fnmatch

def find_txt():
    for file in os.listdir('/opt/reports/'):
        if fnmatch.fnmatch(file, '*.txt'):
            return file

def main():
    while True:
        line = sys.stdin.readline()
        print(line)
        if (m := re.search(r'\|FAILED\s{2}\|[1-9]+[0-9]*\s{68}\|', line)) is not None:
            print(f'Matched group is: {m.group(0)}')
            try:
                with open(f'/opt/reports/{find_txt()}', 'r') as report:
                    for results in report:
                        print(results)
            except FileNotFoundError:
                exit(42)
            exit(1)
        if 'NO VULNERABILITIES FOUND!' in line:
            exit(0)

if __name__ == '__main__':
    main()
