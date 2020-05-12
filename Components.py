import numpy as np
import math
import time
import physicalEngine
import pygame

class RenderSystem:
    def __init__(self, target, image):
        self.target = target
        self.image = pygame.image.load(image).convert_alpha()
    def setImgSize(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
    def render(self, screen):
        screen.blit(self.image, self.target.coordinate)
        #self.target.coordinate 에 render

class TalkSystem:
    def __init__(self):
        pass

class HealthSystem:
    def __init__(self, maxHealth, nowHealth):
        self.maxHealth = maxHealth
        self.nowHealth = nowHealth
    
    def damage(self, damage):
        self.nowHealth -= damage
        if self.nowHealth <1:
            self.kill()
    
    def heal(self, healAmount):
        self.nowHealth += healAmount
        if self.nowHealth > self.maxHealth:
            self.nowHealth = self.maxHealth
        
    def kill(self, target):#target will call died() method
        self.nowHealth = -1
        try:
            target.died()
        except AttributeError:
            pass


class MoveSystem:
    def __init__(self, parent):
        '''parent must be self(actor's self)'''
        self.speedX = 0
        self.speedY = 0
        self.target = parent
        self.angle = 0
    
    def makingAABB(self):
        if type(self.target.collider) is physicalEngine.Circle:
            self.target.collider.AABB = physicalEngine.AABB((self.target.collider.dotList[0][0]-self.target.collider.radius, self.target.collider.dotList[0][1]-self.target.collider.radius), (self.target.collider.dotList[0][0]+self.target.collider.radius, self.target.collider.dotList[0][1]+self.target.collider.radius))
        else:
            xList = []
            yList = []
            for dot in self.target.collider.dotList:
                xList.append(dot[0])
                yList.append(dot[1])

            self.target.collider.AABB = physicalEngine.AABB((min(xList), min(yList)), (max(xList), max(yList)))

    def moveXByAccel(self, acceleration, friction):
        '''
        0<friction<=1
        '''
        self.speedX += acceleration
        self.speedX *= friction
        expression = np.array([self.speedX, 0])
        self.target.coordinate += expression
        for i in range(len(self.target.collider.dotList)):
            self.target.collider.dotList[i] += expression
        self.makingAABB()
    
    def moveYByAccel(self, acceleration, airResistance):
        '''
        0<airResistance<=1
        '''
        self.speedY += acceleration
        self.speedY *= airResistance
        expression = np.array([0, self.speedY])
        self.target.coordinate += expression
        try:
            for i in range(len(self.target.collider.dotList)):
                self.target.collider.dotList[i] += expression
            self.makingAABB()
        except AttributeError:
            pass
    
    def rotate(self, angle):
        self.angle += angle
        try:
            centeroidDot = ((self.target.collider.AABB.minX + self.target.collider.AABB.maxX)/2, (self.target.collider.AABB.minY + self.target.collider.AABB.maxY)/2) 
            if angle == 90:
                expression = np.array([[0, -1], [1, 0]])
            elif angle == 180:
                expression = np.array([[-1, 0], [0, -2]])
            elif angle == 270:
                expression = np.array([[0, 1], [-1, 0]])
            else:
                angle = math.radians(angle)
                expression = np.array([[math.cos(angle), -math.sin(angle)],[math.sin(angle), math.cos(angle)]])

            for i in range(len(self.target.collider.dotList)):
                self.target.collider.dotList[i] = np.dot(expression, (self.dotList[i]-centeroidDot).T) + centeroidDot

            self.makingAABB()
        except AttributeError:
            pass

class RigidPhysicalSystem:
    def __init__(self):
        pass

class EventSystem:
    def __init__(self):
        pass

    def sendEvt(self):
        pass

    def getEvt(self):
        pass

class SoundSystem:
    def __init__(self, fileName):
        self.loopCount = 0
        self.diminishVolumePercentPer100px = 0
        self.volume = 1
        self.clip = pygame.mixer.Sound(fileName)#should be ogg or wav

    def playSound(self, wait):
        self.clip.play()
        
    def stopSound(self):
        self.clip.stop()

    def setVolumeByDistance(self, distance):
        self.clip.set_volume(1-distance*self.diminishVolumePercentPer100px)

    def loopSound(self, loopTime):
        self.loopCount += 1
        if self.loopCount<loopTime or loopTime == -1:
            self.playSound()
            return True
        return False


class Looper:#It helps do loop whitout for, while, time.sleep(). It helps implement function like poision?
    def __init__(self, delayTime, loopNum):
        self.delayTime = delayTime
        self.loopNum = loopNum
        self.loopCount = 0
        self.prevExecutedTime = time.time()

    def loop(self, function):#loop Finished-> return True.
        if self.loopCount>self.loopNum:
            return True
        if time.time()-self.prevExecutedTime>=self.delayTime:
            function()
            self.loopCount += 1
            self.prevExecutedTime = time.time()

    