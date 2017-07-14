#!/bin/python
#-*- conding:utf-8 -*-

import MySQLdb
import argparse

def getColumns(db, tablename):
    lines = db.execute("desc %s"%(tablename))
    results = db.fetchall()
    columns = {}
    for row in results:
        if row[1][:3].lower() == 'int':
            f = int
        elif row[1][:7].lower() == 'varchar':
            f = str
        else:
            raise NotImplementedError

        columns[row[0]] = f
    return columns

def getMaxId(db, tablename):
    db.execute("select max(id) from %s"%(tablename))
    id = db.fetchone()[0]
    return int(id) if id else 0

def insertRow(db, tablename, columns, values):
    sql = "insert into %s(%s) values(%s)"%(tablename,", ".join(columns),", ".join(values))
    db.execute(sql)

def main():
    parser = argparse.ArgumentParser(description="xxx")
    parser.add_argument('--mysql', default='127.0.0.1', help='MySQL database ip/hostname')
    parser.add_argument('--port', default='3306', help='port')
    parser.add_argument('--db', default='yabin', help='database')
    parser.add_argument('-u', required=True, help='user name')
    parser.add_argument('-p', required=True, help='password')
    parser.add_argument('file', help='MAF file (must have header)')
    args = parser.parse_args()
    dbconnect = MySQLdb.connect(host=args.mysql, port=int(args.port), db=args.db, user=args.u, passwd=args.p)
    db = dbconnect.cursor()

    # desc mutation table
    mutationCols = getColumns(db,'mutation')

    # desc sample table
    sampleCols = getColumns(db, 'sample')

    mutationMaxId = getMaxId(db, 'mutation')
    sampleMaxId = getMaxId(db, 'sample')

    # populate MAF data
    with open(args.file) as maf:
        getHeaders = False
        headers = None
        for line in maf:
            if line[0] == "#":
                continue

            if not getHeaders:
                headers = line.strip().split('\t')
                getHeaders = True
                continue

            row = line.strip().split('\t')

            mutationMaxId += 1
            sampleMaxId += 1
            addMutation = [str(mutationMaxId)]
            addMutCols = ['id']
            addSample = [str(sampleMaxId), str(mutationMaxId)]
            addSamCols = ['id', 'mutation_id']

            for header, value in zip(headers, row):
                if header in mutationCols:
                    if mutationCols[header] == str:
                        addMutation.append("'"+value+"'")
                    elif mutationCols[header] == int and not value.isdigit():
                        addMutation.append("NULL")
                    else:
                        addMutation.append(value)
                    addMutCols.append(header)

                if header in sampleCols:
                    if sampleCols[header] == str:
                        addSample.append("'"+value+"'")
                    elif sampleCols[header] == int and not value.isdigit():
                        addSample.append("NULL")
                    else:
                        addSample.append(value)
                    addSamCols.append(header)

            insertRow(db,'mutation',addMutCols,addMutation)
            insertRow(db,'sample',addSamCols,addSample)

    dbconnect.commit()
    dbconnect.close()



if __name__ == '__main__':
    main()