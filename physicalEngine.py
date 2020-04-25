import numpy as np
import math
import sys

class AABB:
    def __init__(self, minCoordinate, maxCoordinate, mass):
        if minCoordinate[0]>maxCoordinate[0] or minCoordinate[1]>maxCoordinate[1]:
            raise Exception("Min값이 Max값보다 큽니다.")

        self.dot1 = np.array([minCoordinate[0], minCoordinate[1]])
        self.dot2 = np.array([maxCoordinate[0], minCoordinate[1]])
        self.dot3 = np.array([maxCoordinate[0], maxCoordinate[1]])
        self.dot4 = np.array([minCoordinate[0], maxCoordinate[1]])

class RotateableAABB:
    def __init__(self, AABBDot1, AABBDot2, mass, angle=0):
        dot1 = np.array([AABBDot1[0], AABBDot1[1]])
        dot2 = np.array([AABBDot2[0], AABBDot1[1]])
        dot3 = np.array([AABBDot2[0], AABBDot2[1]])
        dot4 = np.array([AABBDot1[0], AABBDot2[1]])

        self.centeroidDot = np.array([(AABBDot1[0] + AABBDot2[0])//2, (AABBDot1[1] + AABBDot2[1])//2])
        self.dotList = [dot1, dot2, dot3, dot4]

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
        self.slope = (lineDot1[1]-lineDot2[1])/(lineDot1[0]-lineDot2[0])
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
        meet = [(line2.yIntercept-line1.yIntercept)/(line1.slope-line2.slope), line1.slope*(line2.yIntercept-line1.yIntercept)/(line1.slope-line2.slope) +line1.yIntercept]
        if (line1.dotList[0][0]-meet[0])(line2.dotList[0][0]-meet[0])>0:#두 점 사이에 있으면 x좌표 끼리 뺐을때 하나는 음수, 하나는 양수이기 때문. 딱 꼭짓점이면 0.
            return False
        return True
        
    def getMinkowskiSum(self, polygon1, polygon2):
        pass

    def AABBvsAABB(self, AABB1, AABB2):
        if AABB1.minX>AABB2.maxX or AABB2.minX>AABB1.maxX:
            return False
        elif AABB1.minY>AABB2.maxY or AABB2.minY>AABB1.maxY:
            return False
        else:
            return True

    def isDotInPolygon(self, dot1, polygon1):#오른쪽으로 반직선 그어서 교점이 홀수면 내부, 짝수면 외부에 점이 존재한다는 알고리즘 사용.
        pass


if __name__ == "__main__":
    import time
    FPS = 60
    SCREEN_SIZE = (1920, 1080)
    line1 = Line((0,0), (1,2))
    line2 = Line((3,4), (5, 10))
    c = Collision()
    print(c.LineSegmentvsLineSegment(line1, line2))
    a = RotateableAABB((3,5),(4,8),0)
    a.rotate(80)
    print(a.dotList)
    for i in range(100):
        a.moveX(10,1)
        print(a.dotList)
        time.sleep(0.1)