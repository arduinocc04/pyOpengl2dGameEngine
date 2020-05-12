import numpy as np
import math
import time
import physicalEngine
import pygame

class RenderSystem:
    '''show image on actor's coordinate'''
    def __init__(self, target):
        self.target = target
    def setImage(self, image):
        self.image = pygame.image.load(image).convert_alpha()
    def setImgSize(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
    def render(self, screen):
        screen.blit(self.image, self.target.coordinate)
        #self.target.coordinate 에 render

class TalkSystem:
    '''script.'''
    def __init__(self):
        pass

class HealthSystem:
    '''health system. it can damage, kill other, and heal self'''
    def __init__(self, maxHealth, nowHealth):
        '''if nowHealth>maxHealth -> nowHealth= maxHealth'''
        self.maxHealth = maxHealth
        if nowHealth > maxHealth:
            self.nowHealth = maxHealth
        else:
            self.nowHealth = nowHealth
        self.died = False
    
    def damage(self, damage, target):
        if not target.healthSystem.died:
            target.healthSystem.nowHealth -= damage
            if target.healthSystem.nowHealth <1:
                self.kill(target)
    
    def heal(self, healAmount):
        self.nowHealth += healAmount
        if self.nowHealth > self.maxHealth:
            self.nowHealth = self.maxHealth
    
    def revive(self, healAmount):
        self.died = False
        if healAmount>self.maxHealth:
            healAmount = self.maxHealth
        self.nowHealth = healAmount

    def kill(self, target):#target will call died() method
        self.nowHealth = -1
        self.died = True
        try:
            target.died()
        except AttributeError:
            pass


class MoveSystem:
    '''move system. move target coordinate and collider'''
    def __init__(self, parent):
        '''parent must be self(actor's self)'''
        self.speedX = 0
        self.speedY = 0
        self.target = parent
        self.angle = 0
        self.friction = 1
        self.airResistance = 1
    
    def makingAABB(self):
        if type(self.target.collider) is physicalEngine.Circle:
            self.target.collider.AABB = physicalEngine.AABB((self.target.collider.centerDot[0]-self.target.collider.radius, self.target.collider.centerDot[1]-self.target.collider.radius), (self.target.collider.centerDot[0]+self.target.collider.radius, self.target.collider.centerDot[1]+self.target.collider.radius))
        else:
            xList = []
            yList = []
            for dot in self.target.collider.dotList:
                xList.append(dot[0])
                yList.append(dot[1])

            self.target.collider.AABB = physicalEngine.AABB((min(xList), min(yList)), (max(xList), max(yList)))

    def moveXByAccel(self, acceleration):
        self.speedX += acceleration
        
    def moveYByAccel(self, acceleration):
        self.speedY += acceleration
        
    def jump(self, height):
        self.speedY += height
    
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
    
    def idle(self):
        if abs(self.speedX)<0.0001:
            self.speedX = 0
        if abs(self.speedY)<0.0001:
            self.speedY = 0
        self.speedX *= self.friction
        self.speedY *= self.airResistance

        expression = np.array([self.speedX, self.speedY])
        self.target.coordinate += expression
        if self.target.collider:
            if type(self.target.collider) is physicalEngine.Polygon:
                for i in range(len(self.target.collider.dotList)):
                    self.target.collider.dotList[i] += expression
            else:
                self.target.collider.centerDot += expression
            self.makingAABB()
            
        if self.target.trigger:
            if type(self.target.trigger) is physicalEngine.Polygon:
                for i in range(len(self.target.trigger.component.dotList)):
                    self.target.trigger.component.dotList[i] += expression
            else:
                self.target.trigger.component.centerDot += expression
            self.target.trigger.makingAABB()
        
class RigidPhysicalSystem:
    '''simulation physics'''
    def __init__(self):
        pass

class EventSystem:
    '''may be use for custom event'''
    def __init__(self):
        pass

    def sendEvt(self):
        pass

    def getEvt(self):
        pass

class SoundSystem:
    '''sound system. it can use for bgm or sound effect'''
    def __init__(self, fileName):
        pygame.mixer.init(44100,-16, 2, 2048)
        self.loopCount = 0
        self.diminishVolumePercentPer100px = 0
        self.volume = 1
        self.clip = pygame.mixer.Sound(fileName)#should be ogg or wav

    def playSound(self, wait):
        self.clip.play(wait)
        
    def stopSound(self):
        self.clip.stop()

    def setVolumeByDistance(self, distance):
        self.clip.set_volume(1-math.log10(distance)*self.diminishVolumePercentPer100px)

    def loopSound(self, loopTime):
        self.loopCount += 1
        if self.loopCount<loopTime or loopTime == -1:
            self.playSound()
            return True
        return False

class AI:
    '''useful tool'''
    def __init__(self, parent):
        '''generally parent is self'''
        self.parent = parent

    def chase(self, target, moveSpeed, xDistance):
        '''0<moveSpeed, 0<friction<=1, target means object which chased by parent'''
        targetX, targetY = target.coordinate
        if abs(self.parent.coordinate[0]-targetX) > xDistance:
            if target.mover.speedX>0:#when target see right
                self.parent.mover.moveXByAccel(moveSpeed)
            else:
                self.parent.mover.moveXByAccel(-moveSpeed)

class Looper:#It helps do loop whitout for, while, time.sleep(). It helps implement function like poision?
    '''useful tool'''
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

class Trigger:
    '''use when you need to have two collider.'''
    def __init__(self, component):
        self.component = component
        self.AABB = self.makingAABB()
    
    def makingAABB(self):
        if type(self.component) is physicalEngine.Circle:
            self.AABB = physicalEngine.AABB((self.component.centerDot[0]-self.component.radius, self.component.centerDot[1]-self.component.radius), (self.component.centerDot[0]+self.component.radius, self.component.centerDot[1]+self.component.radius))
        else:
            xList = []
            yList = []
            for dot in self.component.dotList:
                xList.append(dot[0])
                yList.append(dot[1])

            self.AABB = physicalEngine.AABB((min(xList), min(yList)), (max(xList), max(yList)))

    