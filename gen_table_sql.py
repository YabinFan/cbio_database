#!/bin/python
#-*- coding: utf-8 -*-

import argparse

def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description="A smart tool for generating CREATE TABLE sql.")
    parser.add_argument("file", help=".csv filename for input")
    parser.add_argument("-d", help="database name", default='yabin')
    args = parser.parse_args()
    inputfile = args.file

    with open(inputfile, 'rb') as f:
        headers = f.readline().split(',')

    sql = "use %s;"%(args.d)+\
          "\n-- change the table name below"+\
          "\ncreate table [table_name] ("+\
          "\n-- modify the types of fields below"+\
          "\t\n%s"%(' [type],\n\t'.join(headers))+" [type]"\
          "\n-- add constraints below"+\
          "\n\n\n);"
    print sql

if __name__ == '__main__':
    main()