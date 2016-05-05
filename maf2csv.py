#!/bin/python
#-*- coding: utf-8 -*-

import argparse

def MAF2CSV(inputfile, outputfile):
    """

    :param filename: assume file is .maf file
    :return:
    """
    with open(inputfile, 'rb') as infile, open(outputfile, 'w') as outfile:
        for line in infile:
            if line[0] == '#':
                continue
            else:
                outline = line.replace('\t',',').replace('\r\n','\n')
                outfile.write(outline)

def main():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description="A smart tool for parsing .maf data into .csv data.")
    parser.add_argument("maf", help=".maf filename for input")
    args = parser.parse_args()
    inputfile = args.maf
    outputfile = inputfile.split('.')[0]+'.csv'
    MAF2CSV(inputfile, outputfile)
    print 'Converting %s to %s ... DONE'%(inputfile, outputfile)

if __name__ == '__main__':
    main()