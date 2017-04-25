'''
Created on Apr 19, 2017

@author: Steven Proctor
'''
import shapefile
import math



#returns list of all points (as two element tuples) in a shapefile, takes path or shapefile object
def getPoints(shapefile):
    sf=_hi_(shapefile)
    points=[]
    for shp in sf.shapes():
        for p in shp.points:
            points.append(p)
    return points
#takes a path, returns a shapefile or nothing if the path fails
def getShape(path):
    try:
        return shapefile.Reader(path)
    except Exception:
        return None
#Helper Method, lets the others take a path or a 
def _hi_(param):
    if type(param) is str:
        return getShape(param)
    else:
        return param
#returns the topright and bottom left corner points for a rectangle that covers all points, takes a path or a shapefile object
def getBox(shapefile):
    shapefile=_hi_(shapefile)
    px=0
    py=0
    nx=0
    ny=0
    for shp in shapefile.shapes():
        for p in shp.points:
            x=p[0]
            y=p[1]
            if x>px:
                px=x
            if x<nx:
                nx=x
            if y>py:
                py =y 
            if y<ny:
                ny=y 
    return(px,py,nx,ny)

#Returns absolute distance between points
def getDist(a , b):
    x=math.fabs(a[0]-b[0])
    y=math.fabs(a[1]-b[1])
    return math.sqrt(x*x+y*y)

#Returns the area covered by all stations for a particular station coverage radius, takes a path or a shapefile object and a number
def getArea(shapefile,radius):
    
    area=[]
    
    shapefile=_hi_(shapefile)
    for shp in shapefile.shapes():
        for point in shp.points:
            p=[point[0],point[1]]
            while p[0]!=math.floor(p[0]) and p[1]!=math.floor(p[1]):
                p[0]*=10
                p[1]*=10
            for x in range(int(p[0]-radius),int(p[0]+radius)):
                for y in range(int(p[1]-radius),int(p[1]+radius)):
                    if getDist(p, (x,y))<=radius:
                        newpoint=True
                        for rec in area:
                            if rec==(x,y):
                                newpoint=False
                                break
                        if newpoint:
                            area.append((x,y))
    return len(area)

print getArea("C:\\Users\\Steven Proctor\\shapetest\\Metro_Stations_Regional.shp",10)