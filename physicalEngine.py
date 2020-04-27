import numpy as np
import math
import sys
from copy import deepcopy

class AABB:
    def __init__(self, minCoordinate, maxCoordinate, mass):
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

class RotateableAABB:
    def __init__(self, dot1, dot2, dot3, dot4, mass, angle=0):
        dot1 = np.array(dot1)
        dot2 = np.array(dot2)
        dot3 = np.array(dot3)
        dot4 = np.array(dot4)

        self.centeroidDot = np.array([(dot1[0] +dot3[0])/2, (dot1[1] + dot3[1])/2])
        self.dotList = [dot1, dot2, dot3, dot4]
        print('RAABB:', self.dotList)

        minX = min(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0], self.dotList[3][0])
        minY = min(self.dotList[0][1], self.dotList[1][1], self.dotList[2][1], self.dotList[3][1])
        maxX = max(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0], self.dotList[3][0])
        maxY = max(self.dotList[0][1], self.dotList[1][1], self.dotList[2][1], self.dotList[3][1])
        self.AABBForCollision = AABB((minX, minY), (maxX, maxY), 0)

        self.angle = angle
        if angle:
            self.rotate(angle)

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        expression = np.array([speed, 0])
        for i in range(4):
            self.dotList[i] = expression + self.dotList[i]
        self.centeroidDot = expression + self.centeroidDot

        minX = min(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0], self.dotList[3][0])
        maxX = max(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0], self.dotList[3][0])

        if minX < 10:
            self.moveX(acceleration,1)
        if maxX > SCREEN_SIZE[0]-10:
            self.moveX(acceleration,-1)
        return 0

    def rotate(self, angle):
        self.angle += angle
        if angle == 90:
            expression = np.array([[0, -1], [1, 0]])
        elif angle == 180:
            expression = np.array([[-1, 0], [0, -2]])
        elif angle == 270:
            expression = np.array([[0, 1], [-1, 0]])
        else:
            angle = math.radians(angle)
            expression = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
        
        for i in range(4):
            self.dotList[i] = np.dot(expression, (self.dotList[i]-self.centeroidDot).T) + self.centeroidDot

        minX = min(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0], self.dotList[3][0])
        minY = min(self.dotList[0][1], self.dotList[1][1], self.dotList[2][1], self.dotList[3][1])
        maxX = max(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0], self.dotList[3][0])
        maxY = max(self.dotList[0][1], self.dotList[1][1], self.dotList[2][1], self.dotList[3][1])
        self.AABBForCollision = AABB((minX, minY), (maxX, maxY), 0)
        return angle
        

class Triangle:
    def __init__(self, triangleDot1, triangleDot2, triangleDot3, angle=0):
        leftDot = np.array(triangleDot1)
        middleDot = np.array(triangleDot2)
        rightDot = np.array(triangleDot3)
        self.dotList = [leftDot, rightDot, rightDot]
        self.centeroidDot = np.array([(leftDot[0] + rightDot[0] + middleDot[0])/3, (leftDot[1] + rightDot[1] + middleDot[1])/3])
        self.angle = angle
        if angle:
            self.rotate(angle) 

        self.AABBForCollision = AABB((triangleDot1[0], triangleDot3[1]), (triangleDot3[0], triangleDot2[1]), 0)

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        expression = np.array([speed, 0])
        for i in range(3):
            self.dotList[i] = expression + self.dotList[i]
        self.centeroidDot = expression + self.centeroidDot

        minX = min(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0])
        maxX = max(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0])

        if minX < 10:
            self.moveX(acceleration,1)
        if maxX > SCREEN_SIZE[0]-10:
            self.moveX(acceleration,-1)
        return 0

    def rotate(self, angle):
        self.angle += angle
        if angle == 90:
            expression = np.array([[0, -1], [1, 0]])
        elif angle == 180:
            expression = np.array([[-1, 0], [0, -2]])
        elif angle == 270:
            expression = np.array([[0, 1], [-1, 0]])
        else:
            angle = math.radians(angle)
            expression = np.array([[math.cos(angle), -math.sin(angle)],[math.sin(angle), math.cos(angle)]])

        for i in range(3):
            self.dotList[i] = np.dot(expression, (self.dotList[i]-self.centeroidDot).T) + self.centeroidDot

        minX = min(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0])
        minY = min(self.dotList[0][1], self.dotList[1][1], self.dotList[2][1])
        maxX = max(self.dotList[0][0], self.dotList[1][0], self.dotList[2][0])
        maxY = max(self.dotList[0][1], self.dotList[1][1], self.dotList[2][1])
        self.AABBForCollision = AABB((minX, minY), (maxX, maxY), 0)
        return angle




class Circle:
    def __init__(self, centerPosition, radius):
        self.centerDot = np.array(centerPosition)
        self.radius = radius
        self.AABBForCollision = AABB( (self.centerDot[0]-radius, self.centerDot[1]-radius), (self.centerDot[0]+radius, self.centerDot[1]+radius) ,0)

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        expression = np.array([speed, 0])
        self.centerDot = expression + self.centerDot
        self.centeroidDot = expression + self.centeroidDot
        if self.centerDot[0] < 10:
            self.moveX(acceleration,1)
        if self.centerDot[0] > SCREEN_SIZE[0]-10:
            self.moveX(acceleration,-1)
        return 0
    
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

    def getLinevsDotDistance(self, lineDot1, lineDot2, dot1):
        a = lineDot1[0]-lineDot2[0]
        b = lineDot1[1]-lineDot2[1]
        return abs(a*dot1[1] - b*dot1[0] + lineDot2[0]*b - lineDot2[1]*a)/(math.sqrt(a**2 + b**2))#점과 직선사이 공식.

    def LineSegmentvsLineSegment(self, line1, line2):
        if line1.slope == line2.slope:
            return False
        if line1.slope == None:
            meet = [line1.xIntercept, line2.slope*line1.xIntercept + line2.yIntercept]
            line1.slope = 99999999999
        elif line2.slope == None:
            meet = [line2.xIntercept, line1.slope*line2.xIntercept + line1.yIntercept]
            line2.slope = 99999999999
        else:
            meet = [(line2.yIntercept-line1.yIntercept)/(line1.slope-line2.slope), line1.slope*(line2.yIntercept-line1.yIntercept)/(line1.slope-line2.slope) +line1.yIntercept]
        if abs(line1.slope)<abs(line2.slope):#더 완만한 기울기의 선분 고르기.
            if(line1.dotList[1][0]-meet[0])*(line1.dotList[0][0]-meet[0])>0 or (line2.dotList[0][1]-meet[1])*(line2.dotList[1][1]-meet[1])>0:#두 점 사이에 있으면 x좌표 끼리 뺐을때 하나는 음수, 하나는 양수이기 때문. 딱 꼭짓점이면 0. y좌표도 똑같이.
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
        if AABB1.minX>AABB2.maxX or AABB2.minX>AABB1.maxX:
            return False
        elif AABB1.minY>AABB2.maxY or AABB2.minY>AABB1.maxY:
            return False
        else:
            return True

    def isDotInPolygon(self, dot1, polygon1):#오른쪽으로 반직선 그어서 교점이 홀수면 내부, 짝수면 외부에 점이 존재한다는 알고리즘 사용.
        dotLine = Line(dot1, (dot1[0]+100000000, dot1[1]))
        meetCount = 0

        for i in range(len(polygon1.dotList)):
            polygonLine = Line(polygon1.dotList[i-1], polygon1.dotList[i])
            if self.LineSegmentvsLineSegment(dotLine, polygonLine):
                print(f'{dot1}: meet line:/{polygonLine.dotList}')
                meetCount += 1
        print(f'{dot1}: meet {meetCount} time.')
        if meetCount%2 == 1:
            return True

        return False

    def RightTurn(self,p1, p2, p3):
	    if (p3[1]-p1[1])*(p2[0]-p1[0]) >= (p2[1]-p1[1])*(p3[0]-p1[0]):
	    	return False
	    return True

    def GrahamScan(self,P):
	    P.sort(key=lambda dot: dot[0])			# Sort the set of points
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
        if not(reversed):#거꾸로 먼저하고, 이미 겹쳐있다고 판단하면, 그냥 true return.
            if self.PolyvsPoly(polygon2, polygon1, reversed=True):
                return True

        polygon2PointsInPolygon1AABBIndex = self.getPolyDotInOtherPoly(polygon2, polygon1.AABBForCollision)
        if polygon2PointsInPolygon1AABBIndex == []:
            return False

        points = deepcopy(polygon1.dotList)
        for i in polygon2PointsInPolygon1AABBIndex:
            print(f"appended{i}: ", polygon2.dotList[i])
            points.append(polygon2.dotList[i])

        print('points: ', points)
        points = self.GrahamScan(points)
        print('convex_hull: ', points)
        print(f'polygon1 dotList: {polygon1.dotList}')
        if len(points) != len(polygon1.dotList): 
            return False
        return True

if __name__ == "__main__":
    import time
    FPS = 60
    SCREEN_SIZE = (1920, 1080)
    line1 = Line((0,0), (1,2))
    line2 = Line((3,4), (5, 10))
    c = Collision()
    print("lineseg vs lineseg: ", c.LineSegmentvsLineSegment(line1, line2))
    a = RotateableAABB((3,5), (5,5), (5,8), (3,8),0)
    print("dot in poly?: ", c.isDotInPolygon((4,6),a))

    aabb1 = RotateableAABB((2,8), (2,6), (6,6), (6,8), 0)
    aabb2 = RotateableAABB((4,9), (4,7), (8,7), (8,9), 0)
    print("aabb1vsaabb2:", c.PolyvsPoly(aabb1, aabb2))
    '''
    a.rotate(80)
    print(a.dotList)
    for i in range(100):
        a.moveX(10,1)
        print(a.dotList)
        time.sleep(0.1)
    '''