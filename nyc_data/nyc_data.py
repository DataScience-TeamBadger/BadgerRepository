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
budgetM2012 = 8939700000
budgetB2012 = 1191960000
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
    f = open('/home/jd/Documents/School/S6/COSC480/finalproj/ridership_data/metro/nyc_metro.csv', 'w')
    f.write('"YEAR-MONTH","RIDERSHIP","BUDGET (yearly/12)","COVERAGE","POPULATION"\n')
    for i in range(len(datesM)):
        f.write(str(datesM[i]))
        f.write(',')
        f.write(str(ridershipM[i]))
        f.write(',')
        f.write(str(budgetM2012/12))
        f.write(',')
        f.write('<coverage>')
        f.write(',')
        f.write('<popdens>\n')
    f.close()
    #Bus
    f2 = open('/home/jd/Documents/School/S6/COSC480/finalproj/ridership_data/bus/nyc_bus.csv', 'w')
    f2.write('"YEAR-MONTH","RIDERSHIP","BUDGET (yearly/12)","COVERAGE","POPULATION"\n')
    for i in range(len(datesB)):
        f2.write(str(datesB[i]))
        f2.write(',')
        f2.write(str(ridershipB[i]))
        f2.write(',')
        f2.write(str(budgetB2012/12))
        f2.write(',')
        f2.write('<coverage>')
        f2.write(',')
        f2.write('<popdens>\n')
    f2.close()

readDataM('/home/jd/Documents/School/S6/COSC480/finalproj/ridership_data/bus/MTA_Performance_NYCT.csv')
readDataB('/home/jd/Documents/School/S6/COSC480/finalproj/ridership_data/bus/MTA_Performance_NYCT.csv')
writeData()
