import numpy as np
import math
import sys
from copy import deepcopy

class AABB:
    def __init__(self, minCoordinate, maxCoordinate):
        if minCoordinate[0]>maxCoordinate[0] or minCoordinate[1]>maxCoordinate[1]:
            raise Exception("Min값이 Max값보다 큽니다.")

        dot1 = np.array([minCoordinate[0], minCoordinate[1]])
        dot2 = np.array([maxCoordinate[0], minCoordinate[1]])
        dot3 = np.array([maxCoordinate[0], maxCoordinate[1]])
        dot4 = np.array([minCoordinate[0], maxCoordinate[1]])

        self.dotList = [dot1, dot2, dot3, dot4]

        self.minX = min(dot1[0], dot2[0], dot3[0], dot4[0])
        self.maxX = max(dot1[0], dot2[0], dot3[0], dot4[0])
        self.maxY = max(dot1[1], dot2[1], dot3[1], dot4[1])
        self.minY = min(dot1[1], dot2[1], dot3[1], dot4[1])

class Circle:
    def __init__(self, centerPosition, radius):
        self.dotList = [np.array([float(centerPosition[0]), float(centerPosition[1])])]
        self.radius = radius
        self.AABB = AABB( (self.dotList[0][0]-radius, self.dotList[0][1]-radius), (self.dotList[0][0]+radius, self.dotList[0][1]+radius))

class Polygon:
    def __init__(self, pointList, angle=0):
        self.dotList = pointList

        xList = []
        yList = []
        for dot in pointList:
            xList.append(dot[0])
            yList.append(dot[1])

        self.AABB = AABB((min(xList), min(yList)), (max(xList), max(yList)))

    
class Line:
    def __init__(self, lineDot1, lineDot2):
        a = lineDot1[0]-lineDot2[0]
        if a == 0:
            self.slope = None
        else:
            self.slope = (lineDot1[1]-lineDot2[1])/a
        if self.slope == None:
            self.xIntercept = lineDot1[0]
        else:
            self.yIntercept = lineDot1[1]-self.slope*lineDot1[0]
        self.dotList = [np.array(lineDot1), np.array(lineDot2)]


class Collision:
    def __init__(self):
        pass

    def getDotvsDotDistanceSquared(self,dot1, dot2):
        return (dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2

    def getLinevsDotDistance(self, line1, dot1):
        assert type(line1) is Line

        a = line1.dotList[0][0]-line1.dotList[1][0]
        b = line1.dotList[0][1]-line1.dotList[1][1]
        return abs(a*dot1[1] - b*dot1[0] + line1.dotList[1][0]*b - line1.dotList[1][1]*a)/(math.sqrt(a**2 + b**2))#점과 직선사이 공식.

    def LineSegmentvsLineSegment(self, line1, line2):
        assert type(line1) is Line
        assert type(line2) is Line

        if line1.slope == line2.slope:
            return False
        if line1.slope == None:
            meet = [line1.xIntercept, line2.slope*line1.xIntercept + line2.yIntercept]
            line1.slope = 99999999999#x축에 수직인 그래프의 기울기.(대충 큰값 넣은것.)
        elif line2.slope == None:
            meet = [line2.xIntercept, line1.slope*line2.xIntercept + line1.yIntercept]
            line2.slope = 99999999999
        else:
            meet = [(line2.yIntercept-line1.yIntercept)/(line1.slope-line2.slope), line1.slope*(line2.yIntercept-line1.yIntercept)/(line1.slope-line2.slope) +line1.yIntercept]
        if abs(line1.slope)<abs(line2.slope):#더 완만한 기울기의 선분 고르기.
            if(line1.dotList[1][0]-meet[0])*(line1.dotList[0][0]-meet[0])>0 or (line2.dotList[0][1]-meet[1])*(line2.dotList[1][1]-meet[1])>0:
                return False
        else:
            if(line2.dotList[1][0]-meet[0])*(line2.dotList[0][0]-meet[0])>0 or (line1.dotList[0][1]-meet[1])*(line1.dotList[1][1]-meet[1])>0:
                return False
        return True
        
    def getPolyDotInOtherPoly(self, sourcePoly, backGroundPoly):
        polyIndexList = []
        for i in range(len(sourcePoly.dotList)):
            if self.isDotInPolygon(sourcePoly.dotList[i],backGroundPoly):
                polyIndexList.append(i)
        return polyIndexList

    def AABBvsAABB(self, AABB1, AABB2):
        assert type(AABB1) is AABB
        assert type(AABB2) is AABB

        if AABB1.minX>AABB2.maxX or AABB2.minX>AABB1.maxX:
            return False
        if AABB1.minY>AABB2.maxY or AABB2.minY>AABB1.maxY:
            return False
        return True

    def isDotInPolygon(self, dot1, polygon1):#오른쪽으로 반직선 그어서 교점이 홀수면 내부, 짝수면 외부에 점이 존재한다는 알고리즘 사용.
        dotLine = Line(dot1, (dot1[0]+10000, dot1[1]))
        meetCount = 0

        for i in range(len(polygon1.dotList)):
            polygonLine = Line(polygon1.dotList[i-1], polygon1.dotList[i])
            if self.LineSegmentvsLineSegment(dotLine, polygonLine):
                meetCount += 1
        if meetCount%2 == 1:
            return True

        return False

    def RightTurn(self,p1, p2, p3):
	    if (p3[1]-p1[1])*(p2[0]-p1[0]) >= (p2[1]-p1[1])*(p3[0]-p1[0]):
	    	return False
	    return True

    def GrahamScan(self,P):
	    P.sort(key=lambda dot: dot[1])			# Sort the set of points
	    L_upper = [P[0], P[1]]		# Initialize upper part
	    # Compute the upper part of the hull
	    for i in range(2,len(P)):
	    	L_upper.append(P[i])
	    	while len(L_upper) > 2 and not self.RightTurn(L_upper[-1],L_upper[-2],L_upper[-3]):
	    		del L_upper[-2]
	    L_lower = [P[-1], P[-2]]	# Initialize the lower part
	    # Compute the lower part of the hull
	    for i in range(len(P)-3,-1,-1):
	    	L_lower.append(P[i])
	    	while len(L_lower) > 2 and not self.RightTurn(L_lower[-1],L_lower[-2],L_lower[-3]):
	    		del L_lower[-2]
	    del L_lower[0]
	    del L_lower[-1]
	    L = L_upper + L_lower		# Build the full hull
	    return L

    def PolyvsPoly(self, polygon1, polygon2, reversed= False):
        assert type(polygon1) is Polygon
        assert type(polygon2) is Polygon

        if not(reversed):#거꾸로 먼저하고, 이미 겹쳐있다고 판단하면, 그냥 true return.
            if self.PolyvsPoly(polygon2, polygon1, reversed=True):
                return True

        polygon2PointsInPolygon1AABBIndex = self.getPolyDotInOtherPoly(polygon2, polygon1.AABB)
        if polygon2PointsInPolygon1AABBIndex == []:
            return False

        points = deepcopy(polygon1.dotList)
        for i in polygon2PointsInPolygon1AABBIndex:
            points.append(polygon2.dotList[i])

        points = self.GrahamScan(points)
        if len(points) != len(polygon1.dotList): 
            return False
        return True

    def CirclevsCircle(self, circle1, circle2):
        assert type(circle1) is Circle
        assert type(circle2) is Circle

        centerDotDistanceSquared = self.getDotvsDotDistanceSquared(circle1.dotList[0], circle2.dotList[0])
        return ((circle1.radius + circle2.radius)**2-centerDotDistanceSquared)>0

    def PolyvsCircle(self, polygon1, circle1):
        assert type(polygon1) is Polygon
        assert type(circle1) is Circle

        for i in range(len(polygon1.dotList)):
            polygonLine = Line(polygon1.dotList[i-1], polygon1.dotList[i])
            if self.getLinevsDotDistance(polygonLine, circle1.dotList[0]) < circle1.radius:
                return True
        return False

    def ActorvsActor(self, actor1, actor2):
        actor1Component = actor1.collider
        actor2Component = actor2.collider
        if type(actor1Component) is Circle:
            if type(actor2Component) is Circle:
                if self.CirclevsCircle(actor1Component, actor2Component):
                    return True
            else:
                if self.PolyvsCircle(actor2Component, actor1Component):
                    return True
        else:
            if type(actor2Component) is Circle:
                if self.PolyvsCircle(actor1Component, actor2Component):
                    return True
            else:
                if self.PolyvsPoly(actor1Component, actor2Component):
                    return True
        return False
