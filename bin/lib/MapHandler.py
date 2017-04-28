'''
Created on Apr 19, 2017

@author: Steven Proctor
'''
import shapefile
import math
import csv
import re
from decimal import *


#Credit for this function goes to Staale @ http://stackoverflow.com/questions/343865/how-to-convert-from-utm-to-latlng-in-python-or-javascript#344083
#May his name live on forever
#It converts evil utm into beautiful lat long
def utmToLatLng(zone, easting, northing, northernHemisphere=True):
    if not northernHemisphere:
        northing = 10000000 - northing

    a = 6378137
    e = 0.081819191
    e1sq = 0.006739497
    k0 = 0.9996

    arc = northing / k0
    mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

    ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

    ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

    cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
    cc = 151 * math.pow(ei, 3) / 96
    cd = 1097 * math.pow(ei, 4) / 512
    phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

    n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

    r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
    fact1 = n0 * math.tan(phi1) / r0

    _a1 = 500000 - easting
    dd0 = _a1 / (n0 * k0)
    fact2 = dd0 * dd0 / 2

    t0 = math.pow(math.tan(phi1), 2)
    Q0 = e1sq * math.pow(math.cos(phi1), 2)
    fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

    fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

    lof1 = _a1 / (n0 * k0)
    lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
    lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
    _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
    _a3 = _a2 * 180 / math.pi

    latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

    if not northernHemisphere:
        latitude = -latitude

    longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

    return (latitude, longitude)


#returns list of all points (as two element tuples) in a parsefile, takes path or parsefile object
def getPoints(parsefile):
    sflst=_hi_(parsefile)
    x=[]
    y=[]
    for sf in sflst:
        for p in sf:
            x.append(p[0])
            y.append(p[1])
    return [x,y]
#takes a path, returns a parsefile or nothing if the path fails
def getShape(path):
    #try:
    points=[]
    for shp in shapefile.Reader(path).shapes():
        for p in shp.points:
            points.append(p)
    return points
    #except Exception:
        #print path +"\t"+"Not found!"
        #return None
#Helper Method, lets the others take a path or a 
def _hi_(param):
    if type(param) is str:
        temp = param[param.index(".")+4:].strip()
        param =param[:param.index(".")+4].strip()
        temp= temp.split(" ")
        if param[-4:] == ".csv":
            colnumLat=int(temp[0])
            colnumLong=int(temp[1])
            points = []
            head=True
            for s in csv.reader(open(param)):
                if head:
                    head=False
                    continue
                points.append((s[colnumLat],s[colnumLong]))
            return [points]
        if param[-4:] ==".kml":
            kmlName=temp[0]
            data = open(param).read()
            matches = re.findall("<"+kmlName+">.+?</"+kmlName+">", data, re.DOTALL)
            points=[]
            for m in matches:
                temp = m[len(kmlName)+2:-len(kmlName)+2].split(",")
                points.append((float(temp[0]),float(temp[1])))
            return [points]
        return [getShape(param)]
    elif type (param) is list:
        out = []
        for p in param:
            out.append(_hi_(p))
        return out
    else:
        return [param]


#Returns absolute distance between points
def getDist(a , b,dd=0):
    getcontext().prec=32
    dd=math.pow(10,dd)
    x=Decimal(((a[0]*(111.320*math.cos(a[1])))-(b[0]/dd*(111.320*math.cos(b[1]/dd)))))
    y=Decimal((a[1]*110.574)-(b[1]/dd*110.574))
    return Decimal(math.sqrt(x*x+y*y))

#Returns the area covered by all stations for a particular station coverage radius, takes a path or a parsefile object and a number
def getArea(shapefilelst,radius,decimaldigits=14.0,utmZone=None,utmNorHemi=True,colnumLat=0,colnumLong=1,kmlName="coordinates"):
    area=[]
    decimaldigits=decimaldigits*1.0
    shapefilelst=_hi_(shapefilelst,colnumLat,colnumLong,kmlName)
    for parsefile in shapefilelst:
        for point in parsefile:
            p=[]
            if utmZone==None:
                p=[point[0],point[1]]
            else:
                p=utmToLatLng(utmZone, point[0], point[1], utmNorHemi)
                p=[p[0],p[1]]
            for x in range(int((p[0]-radius)*decimaldigits),int(p[0]+radius)*decimaldigits):
                for y in range(int((p[1]-radius)*decimaldigits),int((p[1]+radius)*decimaldigits)):
                    if getDist(p, (x,y),decimaldigits)<=radius:
                        newpoint=True
                        for rec in area:
                            if rec==(x,y):
                                newpoint=False
                                break
                        if newpoint:
                            area.append((x,y))
    return len(area)