
import glfw
from OpenGL.GL import *
import numpy as np
import math
import sys

class MinBiggerThanMaxError(Exception):
    def __init__(self):
        super().__init__("Min값이 Max값보다 큽니다.")


class AABB:
    def __init__(self, minCoordinate, maxCoordinate, mass):
        self.minX = minCoordinate[0]
        self.minY = minCoordinate[1]
        self.maxX = maxCoordinate[0]
        self.maxY = maxCoordinate[1]
        if self.minX>self.maxX or self.minY>self.maxY:
            raise MinBiggerThanMaxError

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        self.minX += speed
        self.maxX += speed

        while self.minX<10:
            self.moveX(acceleration,1)
        while self.maxX>SCREEN_SIZE[0]-10:
            self.moveX(acceleration,-1)

class RightTriAngle:
    def __init__(self, leftCoordinate, rightCoordinate):
        self.leftX = leftCoordinate[0]
        self.leftY = leftCoordinate[1]
        self.rightX = rightCoordinate[0]
        self.rightY = rightCoordinate[1]
        self.height = abs(self.leftY-self.rightY)
        self.width = self.rightX-self.leftX
        if self.width<0:
            raise Exception("좌표 오류: 왼쪽 x좌표> 오른쪽 x좌표")
        self.flag = False#빗변 기울기가 음수.
        if self.rightY>self.leftY:
            self.flag = True
        
        if flag:
            self.AABBForCollision = AABB(leftCoordinate, rightCoordinate, 0)
        else:
            self.AABBForCollision = AABB((self.leftX,self.rightY), (self.rightX, self.leftY))
        

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        self.leftX += speed
        self.rightX += speed

        while self.minX<10:
            self.moveX(acceleration,1)
        while self.maxX>SCREEN_SIZE[0]-10:
            self.moveX(acceleration,-1)

    def isDotUnderHypotenuse(self, dot1):
        x2MinusX1 = self.rightX-self.leftX
        y2MinusY1 = self.rightY-self.leftY
        if (y2MinusY1/x2MinusX1)*(dot1[0]-self.leftX) + self.leftY >dot1[1]:
            return True
        return False



class Circle:
    def __init__(self, position, radius):
        self.centerX = position[0]
        self.centerY = position[1]
        self.radius = radius
        self.AABBForCollision = AABB( (self.centerX-radius, self.centerY-radius), (self.centerX+radius, self.centerY+radius) )

    def moveX(self, acceleration, direction):#right->1, left->-1 등속 직선 운동.
        global FPS,SCREEN_SIZE
        speed = direction*(acceleration)
        self.centerX += speed

        while self.centerX-self.radius<10:
            self.moveX(acceleration,1)
        while self.centerX+self.radius>SCREEN_SIZE[0]-10:
            self.moveX(acceleration,-1)

class Collision:
    def __init__(self):
        pass
    def getDotvsDotDistance(self,dot1, dot2):
        return(math.sqrt((dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2))
    def getLinevsDotDistance(self, lineDot1, lineDot2, dot1):
        a = lineDot1[0]-lineDot2[0]
        b = lineDot1[1]-lineDot2[1]
        return abs(a*dot1[1] - b*dot1[0] + lineDot2[0]*b - lineDot2[1]*a)/(math.sqrt(a**2 + b**2))#점과 직선사이 공식.

    def AABBvsAABB(self, AABB1, AABB2):
        if AABB1.minX>AABB2.maxX or AABB2.minX>AABB1.maxX:
            return False
        elif AABB1.minY>AABB2.maxY or AABB2.minY>AABB1.maxY:
            return False
        else:
            return True
    def CirclevsCircle(self, Circle1, Circle2):
        if self.getDistance((Circle1.centerX, Circle1.centerY), (Circle2.centerX, Circle2.centerY)) < Circle1.radius + Circle2.radius:
            return True
        return False
    def AABBvsCircle(self, AABB1, Circle1):
        if AABB1.maxY<Circle1.centerY-Circle1.radius or AABB1.minY > Circle1.centerY+Circle1.radius:
            return False
        elif AABB1.maxX<Circle1.centerX-Circle1.radius or AABB1.minX>Circle1.centerX+Circle1.radius:
            return False
        else:
            return True
    def AABBvsRightTriangle(self, AABB1, Triangle1):
        if self.AABBvsAABB(AABB1, Triangle1.AABBForCollision):
            if Triangle1.flag:
                if Triangle1.isDotUnderHypotenuse((AABB1.maxX, AABB1.minY)):
                   return True
            else:
                if Triangle1.isDotUnderHypotenuse((AABB1.minX, AABB1.minY)):
                    return True
        return False
    def CirclevsRightTriangle(self, Circle1, Triangle1):
        if self.AABBvsAABB(Circle1.AABBForCollision, Triangle1.AABBForCollision):
            if self.AABBvsCircle(Triangle1.AABBForCollision, Circle1):
                if Triangle1.isDotUnderHypotenuse((Circle1.centerX, Circle1.centerY)):
                    return True
                else:
                    if self.getLinevsDotDistance((Triangle1.leftX, Triangle1.leftY), (Triangle1.rightX, Triangle1.rightY), (Circle1.centerX, Circle1.centerY)) < Circle1.radius:
                        return True
        return False
                    


#TEST`
a = AABB((4,40), (50,400), 1)
b = AABB((2,3),(5,6), 1)
c = Collision()
print(c.AABBvsAABB(a,b))
d = Circle((10,500), 40)
e = Circle((2,4), 8)
print(c.CirclevsCircle(d,e))
print(c.AABBvsCircle(a,d))
print(c.AABBvsCircle(a,e))
print(c.AABBvsCircle(b,d))
print(c.AABBvsCircle(b,e))

FPS = 60 
SCREEN_SIZE = (1920, 1080)