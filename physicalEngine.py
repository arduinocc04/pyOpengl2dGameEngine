import numpy as np
import math
import sys

class MinBiggerThanMaxError(Exception):
    def __init__(self):
        super().__init__("Min값이 Max값보다 큽니다.")


class AABB:
    def __init__(self, minCoordinate, maxCoordinate, mass):
        if minCoordinate[0]>maxCoordinate[0] or minCoordinate[1]>maxCoordinate[1]:
            raise MinBiggerThanMaxError

        self.dot1 = np.array([minCoordinate[0], minCoordinate[1]])
        self.dot2 = np.array([maxCoordinate[0], minCoordinate[1]])
        self.dot3 = np.array([maxCoordinate[0], maxCoordinate[1]])
        self.dot4 = np.array([minCoordinate[0], maxCoordinate[1]])

class RotateableAABB:
    def __init__(self, minCoordinate, maxCoordinate, mass, angle=0):
        self.dot1 = np.array([minCoordinate[0], minCoordinate[1]])
        self.dot2 = np.array([maxCoordinate[0], minCoordinate[1]])
        self.dot3 = np.array([maxCoordinate[0], maxCoordinate[1]])
        self.dot4 = np.array([minCoordinate[0], maxCoordinate[1]])
        self.angle = angle
        if angle:
            self.rotate(angle)

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        expression = np.array([speed, 0])
        self.dot1 = expression + self.dot1
        self.dot2 = expression + self.dot2
        self.dot3 = expression + self.dot3
        self.dot4 = expression + self.dot4

        minX = min(self.dot1[0], self.dot2[0], self.dot3[0], self.dot4[0])
        maxX = max(self.dot1[0], self.dot2[0], self.dot3[0], self.dot4[0])

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

        self.dot1 = np.dot(expression, self.dot1.T)
        self.dot2 = np.dot(expression, self.dot2.T)
        self.dot3 = np.dot(expression, self.dot3.T)
        self.dot4 = np.dot(expression, self.dot4.T)

        for i in range(2):
            self.dot1[i] = round(self.dot1[i])
            self.dot2[i] = round(self.dot2[i])
            self.dot3[i] = round(self.dot3[i])
            self.dot4[i] = round(self.dot4[i])

        minX = min(self.dot1[0], self.dot2[0], self.dot3[0], self.dot4[0])
        minY = min(self.dot1[1], self.dot2[1], self.dot3[1], self.dot4[1])
        maxX = max(self.dot1[0], self.dot2[0], self.dot3[0], self.dot4[0])
        maxY = max(self.dot1[1], self.dot2[1], self.dot3[1], self.dot4[1])
        self.AABBForCollision = AABB((minX, minY), (maxX, maxY), 0)
        return angle
        

class RightTriangle:
    def __init__(self, leftCoordinate, rightCoordinate, angle=0):
        self.leftDot = np.array(leftCoordinate)
        self.rightDot = np.array(rightCoordinate)
        self.otherDot = np.array(rightCoordinate[0], leftCoordinate[1])
        self.angle = angle
        if angle:
            self.rotate(angle)
        self.height = abs(self.leftDot[1]-self.rightDot[1])
        self.width = self.rightDot[0]-self.leftDot[0]

        if self.width<0:
            raise Exception("좌표 오류: 왼쪽 x좌표> 오른쪽 x좌표")
        self.flag = False#빗변 기울기가 음수.
        if self.rightDot[1]>self.leftDot[1]:
            self.flag = True
        
        if self.flag:
            self.AABBForCollision = AABB(leftCoordinate, rightCoordinate, 0)
        else:
            self.AABBForCollision = AABB((self.leftDot[0], self.rightDot[1]), (self.rightDot[0], self.leftDot[1]), 0)
        

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        expression = np.array([speed, 0])
        self.leftDot = expression + self.leftDot
        self.rightDot = expression + self.rightDot
        self.otherDot = expression + self.otherDot

        minX = min(self.leftDot[0], self.rightDot[0], self.otherDot[0])
        maxX = max(self.leftDot[0], self.rightDot[0], self.otherDot[0])

        if minX < 10:
            self.moveX(acceleration,1)
        if maxX > SCREEN_SIZE[0]-10:
            self.moveX(acceleration,-1)
        return 0

    def isDotUnderHypotenuse(self, dot1):
        x2MinusX1 = self.rightX-self.leftX
        y2MinusY1 = self.rightY-self.leftY
        if (y2MinusY1/x2MinusX1)*(dot1[0]-self.leftX) + self.leftY >dot1[1]:
            return True
        return False

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

        self.leftDot = np.dot(expression, self.leftDot.T)
        self.rightDot = np.dot(expression, self.rightDot.T)
        self.otherDot = np.dot(expression, self.otherDot.T)
        for i in range(2):
            self.leftDot[i] = round(self.leftDot[i])
            self.rightDot[i] = round(self.rightDot[i])
            self.otherDot[i] = round(self.otherDot[i])
        xList = [self.leftDot[0], self.rightDot[0], self.otherDot[0]]
        yList = [self.leftDot[1], self.rightDot[1], self.otherDot[1]]
        self.AABBForCollision = AABB((min(xList), min(yList)), (max(xList), max(yList)), 0)
        return angle


class Triangle:
    def __init__(self, leftCoordinate, middleCoordinate, rightCoordinate, angle=0):
        self.leftDot = np.array(leftCoordinate)
        self.middleDot = np.array(middleCoordinate)
        self.rightDot = np.array(rightCoordinate)
        self.angle = angle
        if angle:
            self.rotate(angle) 

        if leftCoordinate[1] != rightCoordinate[1] or middleCoordinate[1] <= rightCoordinate[1] or leftCoordinate[0] >= middleCoordinate[0] or middleCoordinate[0] >= rightCoordinate[0]:
            raise Exception("좌표 값이 이상합니다. 밑변이 ㅡ와 같은 모양이여야 하고(왼쪽 y == 오른쪽 y), 가운데 y가 가장 커야 하며, (왼쪽, 가운데, 오른쪽)순서로 인수를 입력해야 합니다.")
        
        self.AABBForCollision = AABB((leftCoordinate[0], rightCoordinate[1]), (rightCoordinate[0], middleCoordinate[1]), 0)
        self.leftRightTriangleForCollision = RightTriangle(leftCoordinate, middleCoordinate)
        self.rightRightTriangleForCollision = RightTriangle(middleCoordinate, rightCoordinate)

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        expression = np.array([speed, 0])
        self.leftDot = expression + self.leftDot
        self.middleDot = expression + self.middleDot
        self.rightDot = expression + self.rightDot

        minX = min(self.leftDot[0], self.rightDot[0], self.middleDot[0])
        maxX = max(self.leftDot[0], self.rightDot[0], self.middleDot[0])

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

        self.leftDot = np.dot(expression, self.leftDot.T)
        self.middleDot = np.dot(expression, self.middleDot.T)
        self.rightDot = np.dot(expression, self.rightDot.T)

        for i in range(2):
            self.leftDot[i] = round(self.leftDot[i])
            self.rightDot[i] = round(self.rightDot[i])
            self.middleDot[i] = round(self.middleDot[i])

        xList = [self.leftDot[0], self.rightDot[0], self.middleDot[0]]
        yList = [self.leftDot[1], self.rightDot[1], self.middleDot[1]]
        self.AABBForCollision = AABB((min(xList), min(yList)), (max(xList), max(yList)), 0)
        return angle




class Circle:
    def __init__(self, position, radius):
        self.centerDot = np.array(position)
        self.radius = radius
        self.AABBForCollision = AABB( (self.centerX-radius, self.centerY-radius), (self.centerX+radius, self.centerY+radius) ,0)

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        expression = np.array([speed, 0])
        self.centerDot = expression + self.centerDot
        if self.centerDot[0] < 10:
            self.moveX(acceleration,1)
        if self.centerDot[0] > SCREEN_SIZE[0]-10:
            self.moveX(acceleration,-1)
        return 0

class Collision:
    def __init__(self):
        pass

    def getDotvsDotDistance(self,dot1, dot2):
        return(math.sqrt((dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2))

    def getLinevsDotDistance(self, lineDot1, lineDot2, dot1):
        a = lineDot1[0]-lineDot2[0]
        b = lineDot1[1]-lineDot2[1]
        return abs(a*dot1[1] - b*dot1[0] + lineDot2[0]*b - lineDot2[1]*a)/(math.sqrt(a**2 + b**2))#점과 직선사이 공식.

    def LinevsLine(self, line1, line2):#일차방정식으로 넣기.
        pass

    def AABBvsAABB(self, AABB1, AABB2):
        if AABB1.minX>AABB2.maxX or AABB2.minX>AABB1.maxX:
            return False
        elif AABB1.minY>AABB2.maxY or AABB2.minY>AABB1.maxY:
            return False
        else:
            return True
    def CirclevsCircle(self, Circle1, Circle2):
        if self.getDotvsDotDistance((Circle1.centerX, Circle1.centerY), (Circle2.centerX, Circle2.centerY)) < Circle1.radius + Circle2.radius:
            return True
        return False
    def AABBvsCircle(self, AABB1, Circle1):
        if AABB1.maxY<Circle1.centerY-Circle1.radius or AABB1.minY > Circle1.centerY+Circle1.radius:
            return False
        elif AABB1.maxX<Circle1.centerX-Circle1.radius or AABB1.minX>Circle1.centerX+Circle1.radius:
            return False
        else:
            return True
    def AABBvsRightTriangle(self, AABB1, RightTriangle1):
        if self.AABBvsAABB(AABB1, RightTriangle1.AABBForCollision):
            if AABB1.minX<= RightTriangle1.leftX and AABB1.maxX>= RightTriangle1.rightX:
                return True
            if RightTriangle1.flag:
                if RightTriangle1.isDotUnderHypotenuse((AABB1.maxX, AABB1.minY)):
                   return True
            else:
                if RightTriangle1.isDotUnderHypotenuse((AABB1.minX, AABB1.minY)):
                    return True
        return False
    def CirclevsRightTriangle(self, Circle1, RightTriangle1):
        if self.AABBvsAABB(Circle1.AABBForCollision, RightTriangle1.AABBForCollision):
            if self.AABBvsCircle(RightTriangle1.AABBForCollision, Circle1):
                if RightTriangle1.isDotUnderHypotenuse((Circle1.centerX, Circle1.centerY)):
                    return True
                else:
                    if self.getLinevsDotDistance((RightTriangle1.leftX, RightTriangle1.leftY), (RightTriangle1.rightX, RightTriangle1.rightY), (Circle1.centerX, Circle1.centerY)) < Circle1.radius:
                        return True
        return False
    def AABBvsTriangle(self, AABB1, Triangle1):
        if self.AABBvsAABB(AABB1, Triangle1.AABBForCollision):
            if AABB1.minX<= Triangle1.leftX and AABB1.maxX>= Triangle1.rightX:
                return True
            if self.AABBvsRightTriangle(AABB1, Triangle1.leftRightTriangleForCollision):
                return True
            if self.AABBvsRightTriangle(AABB1, Triangle1.rightRightTriangleForCollision):
                return True
            if Triangle1.leftRightTriangleForCollision.isDotUnderHypotenuse(((AABB1.minX + AABB1.maxX)/2, AABB1.minY)):
                return True
            if Triangle1.rightRightTriangleForCollision.isDotUnderHypotenuse(((AABB1.minX + AABB1.maxX)/2, AABB1.minY)):
                return True
        return False

if __name__ == "__main__":
    import time
    FPS = 60
    SCREEN_SIZE = (1920, 1080)
    a = RotateableAABB((3,5),(4,8),0)
    a.rotate(80)
    print(a.dot1, a.dot2, a.dot3, a.dot4)
    for i in range(100):
        a.moveX(10,1)
        print(a.dot1, a.dot2, a.dot3, a.dot4)
        time.sleep(0.1)