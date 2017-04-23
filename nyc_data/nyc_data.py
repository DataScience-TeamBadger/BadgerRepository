#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 13:59:05 2017

@author: jd
"""
#Lists
datesM = []
ridershipM = []
datesB = []
ridershipB = []
#Known variables
budgetM2008 = 1848450000
budgetB2008 = 246460000
budgetM2009 = 1875150000
budgetB2009 = 250020000
budgetM2010 = 1906350000
budgetB2010 = 254180000
budgetM2011 = 2056500000
budgetB2011 = 274200000
budgetM2012 = 2114100000
budgetB2012 = 281880000
budgetM2013 = 2144100000
budgetB2013 = 285880000
budgetM2014 = 2174100000
budgetB2014 = 289880000
budgetM2015 = 2204100000
budgetB2015 = 293880000
budgetM2016 = 2234100000
budgetB2016 = 297880000
"""Unknown variables
areaM = 
areaB = 
popM = 
popB = 
"""

def readDataM(csv):
    f = open(csv, "r")
    f.readline()
    for line in f:
        splitline = line.split(",")
        if int(splitline[0]) == 103929:
            datesM.append(str(splitline[17]) + '-' + str(splitline[18]))
            ridershipM.append(int(splitline[22][:-5]))

def readDataB(csv):
    f = open(csv, "r")
    f.readline()
    for line in f:
        splitline = line.split(",")
        if int(splitline[0]) == 204043:
            datesB.append(str(splitline[17]) + '-' + str(splitline[18]))
            ridershipB.append(int(splitline[22][:-5]))
        
def writeData():
    #Metro
    f = open('/home/jd/Documents/School/S6/COSC480/finalproj/ridership_data/output/nyc_metro.csv', 'w')
    f.write('"YEAR-MONTH","RIDERSHIP","BUDGET (yearly/12)","COVERAGE","POPULATION"\n')
    for i in range(len(datesM)):
        f.write(str(datesM[i]))
        f.write(',')
        f.write(str(ridershipM[i]))
        f.write(',')
        curryear = datesM[i][:4]
        if curryear == '2008':
            f.write(str(budgetM2008/12))
        elif curryear == '2009':
            f.write(str(budgetM2009/12))
        elif curryear == '2010':
            f.write(str(budgetM2010/12))
        elif curryear == '2011':
            f.write(str(budgetM2011/12))
        elif curryear == '2012':
            f.write(str(budgetM2012/12))
        elif curryear == '2013':
            f.write(str(budgetM2013/12))
        elif curryear == '2014':
            f.write(str(budgetM2014/12))
        elif curryear == '2015':
            f.write(str(budgetM2015/12))
        elif curryear == '2016':
            f.write(str(budgetM2016/12))
        f.write(',')
        f.write('<coverage>')
        f.write(',')
        f.write('<popdens>\n')
    f.close()
    #Bus
    f2 = open('/home/jd/Documents/School/S6/COSC480/finalproj/ridership_data/output/nyc_bus.csv', 'w')
    f2.write('"YEAR-MONTH","RIDERSHIP","BUDGET (yearly/12)","COVERAGE","POPULATION"\n')
    for i in range(len(datesB)):
        f2.write(str(datesB[i]))
        f2.write(',')
        f2.write(str(ridershipB[i]))
        f2.write(',')
        curryear = datesB[i][:4]
        if curryear == '2008':
            f2.write(str(budgetB2008/12))
        elif curryear == '2009':
            f2.write(str(budgetB2009/12))
        elif curryear == '2010':
            f2.write(str(budgetB2010/12))
        elif curryear == '2011':
            f2.write(str(budgetB2011/12))
        elif curryear == '2012':
            f2.write(str(budgetB2012/12))
        elif curryear == '2013':
            f2.write(str(budgetB2013/12))
        elif curryear == '2014':
            f2.write(str(budgetB2014/12))
        elif curryear == '2015':
            f2.write(str(budgetB2015/12))
        elif curryear == '2016':
            f2.write(str(budgetB2016/12))
        f2.write(',')
        f2.write('<coverage>')
        f2.write(',')
        f2.write('<popdens>\n')
    f2.close()

readDataM('/home/jd/Documents/School/S6/COSC480/finalproj/ridership_data/bus/MTA_Performance_NYCT.csv')
readDataB('/home/jd/Documents/School/S6/COSC480/finalproj/ridership_data/bus/MTA_Performance_NYCT.csv')
writeData()
