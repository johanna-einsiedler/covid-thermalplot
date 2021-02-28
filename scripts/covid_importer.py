__author__ = 'johanna'

import csv
import argparse

import sqlite3

parser = argparse.ArgumentParser(description='')
parser.add_argument('--basedir', default='')
parser.add_argument('--outputdir', default='../sqlite/')
parser.add_argument('--db', default='data.db')
parser.add_argument('--file', default="myfile.csv")
parser.add_argument('--column', default="col_name")
parser.add_argument('--clear', action='store_true')
args = parser.parse_args()

columns_name = ['confirmed', 'deaths', 'recovered']
columns_type = ['int', 'int','int']

if args.file == 'myfile.csv':
    csv_name = '../data_transformed/data_'+ str(args.column) + '.csv'
else:
    csv_name = args.file

with sqlite3.connect(args.outputdir + args.db) as db:

    columns = []
    i=0
    for c in columns_name:
        columns.append(columns_name[i] + ' ' + columns_type[i])
        i+=1

    columns_str = ', '.join(columns)

    db.execute('CREATE TABLE IF NOT EXISTS covid(key text, ts text, ' + columns_str + ', PRIMARY KEY (key, ts) ON CONFLICT IGNORE )')
    db.execute('CREATE INDEX IF NOT EXISTS covid_key on covid(key)')
    db.execute('CREATE INDEX IF NOT EXISTS covid_ts on covid(ts)')

    def to_row(r):
        print (r)
        key = r[1].replace('"', '').replace('"', '')
        ts =  r[2].replace('"', '').replace('"', '')
        try:
            val = float(r[3])
        except ValueError:
            val = float('NaN')
            
        return val ,key, ts
        #return key, ts, val


    column = args.column
    
    #with open(args.basedir + args.file,'r') as f:
    with open(args.basedir + csv_name,'r') as f:
        
        
        it = (r for (i,r) in enumerate(csv.reader(f,delimiter=',')) if i > 0) # skip first row (header)
        #r = to_row(it.next())
        #print it.next(), r,r[1],r[1] in keys
        #print(it)
        for ri in (to_row(r) for r in it):
            
            #if ri[1] is not None:
                #print (ri)
        
            
            db.execute('UPDATE covid SET '+column+' = ? WHERE key = ? AND ts = ?', ri)
            db.execute('INSERT OR IGNORE INTO covid('+column+',key,ts) VALUES(?,?,?)', ri)
            
            #db.commit()
        #db.executemany('UPDATE air SET temperature = ? WHERE key = ? AND ts = ?',
        db.commit()
