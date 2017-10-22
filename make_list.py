#!/usr/bin/env python

import glob
import csv


shopping = { "Tesco":dict(), "Home":dict(), "Real Foods":dict(), "Bakery":dict(),
        "Sainsburys":dict(), "Costco":dict(), "Global":dict(), "Butchers":dict() }

for file in glob.glob("list.csv"):
    with open(file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, dialect='excel')
        for row in csvreader:
            if len(row) >= 5:
                #if row[1] and row[4] and row[5] == "Tesco":
                if row[1] and row[4] and row[5]:
     #               print "Adding %s %s %s" % (row[3], row[4], row[1])
                    key = "%s-%s" % (row[1], row[4])
                        
                    value_f = 0
                    try:
                        value_f = float(row[3])
                    except ValueError:
                        pass

                    #print row[3]
                    try: 
                        if key in shopping[row[5]].keys():
                            shopping[row[5]][key] = shopping[row[5]][key] + value_f
                        else:
                            shopping[row[5]][key] = value_f
                    except KeyError:
                        print "key error %s" % (row[5])


print

for shop in shopping:
    print shop
    print "----------------"
    print 

    #print shopping[shop]
    for key in sorted(shopping[shop]):
        try:
            (item, unit) = key.rsplit('-', 1)
        except ValueError:
            print "WARNING Can't parse %s" % (key)

        print "    [ ] %8.2f %-11s %s" % (float(shopping[shop][key]), unit, item) 
