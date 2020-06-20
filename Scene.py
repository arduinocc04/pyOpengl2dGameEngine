import time
import PhysicalEngine
import GameObject
import Components
import pygame
from copy import deepcopy
'''
characterObjList[0]이 무조건 Player
좌표는 무조건 []로 입력. !tuple
'''
class Scene:
    def __init__(self, screen, SCREEN_SIZE, FPS, debugLevel = 1):
        pygame.init()
        self.groundObjList = []
        self.characterObjList = []
        self.collision = PhysicalEngine.Collision()
        self.SCREEN_SIZE = SCREEN_SIZE
        self.screen = screen
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.screenAABB = PhysicalEngine.AABB([0,0], SCREEN_SIZE)
        self.font = pygame.font.SysFont('malgungothic', 20)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.VIOLET = (128, 116, 206)
        self.AQUA = (0, 255, 255)
        self.debugLevel = debugLevel
        if debugLevel >=2:
            self.rays = []
    
    def addGroundObj(self, groundObj):
        self.groundObjList.append(groundObj)
        
    def addCharacterObj(self, characterObj):
        self.characterObjList.append(characterObj)
        
    def callUpdate(self):
        for obj in self.characterObjList:
            obj.update()

    def handleY(self, dot):
        return dot[0], self.SCREEN_SIZE[1]-dot[1]
        
    def colliderCollisionCheck(self):
        for obj in self.characterObjList:
            if self.collision.AABBvsAABB(self.screenAABB, obj.collider.AABB):
                if obj.collider:#collision detection.if collided, call collided().(characterObject)
                    if 'g' in obj.colliderSetting:
                        for ground in self.groundObjList:
                            if self.collision.AABBvsAABB(obj.collider.AABB, ground.collider.AABB):
                                if self.collision.isAABBCompAABB(obj.collider.AABB, ground.collider.AABB):
                                    obj.collided(ground)
                                else:
                                    if self.collision.ActorvsActor(obj.collider.component, ground.collider.component):
                                        obj.collided(ground)

                    if 'c' in obj.colliderSetting:
                        for otherObj in self.characterObjList:
                            if otherObj != obj and otherObj.collider and otherObj.allowCharacterColliding:
                                if self.collision.AABBvsAABB(obj.collider.AABB, otherObj.collider.AABB):
                                    if self.collision.isAABBCompAABB(obj.collider.AABB, otherObj.collider.AABB):
                                        obj.collided(otherObj)
                                        otherObj.collided(obj)
                                    else:
                                        if self.collision.ActorvsActor(obj.collider.component, otherObj.collider.component):
                                            obj.collided(otherObj)
                                            otherObj.collided(obj)
                                            
    def triggerCollisionCheck(self):
        for obj in self.characterObjList:
            if obj.trigger:#trigger collision detection
                    if 'p' in obj.triggerSetting:
                        if not obj is self.characterObjList[0] and self.characterObjList[0].collider:
                            if self.collision.AABBvsAABB(obj.trigger.AABB, self.characterObjList[0].collider.AABB):
                                if self.collision.isAABBCompAABB(obj.trigger.AABB, self.characterObjList[0].collider.AABB):
                                    obj.triggerCollided(self.characterObjList[0])
                                else:
                                    if self.collision.ActorvsActor(obj.trigger.component, self.characterObjList[0].collider.component):
                                        obj.triggerCollided(self.characterObjList[0])

                    if 'c' in obj.triggerSetting:
                        for otherObj in characterObjList:
                            if otherObj != obj and otherObj.collider:
                                if self.collision.AABBvsAABB(obj.trigger.AABB, otherObj.collider.AABB):
                                    if self.collision.isAABBCompAABB(obj.trigger.AABB, otherObj.collider.AABB):
                                        obj.triggerCollided(otherObj)
                                    else:
                                        if self.collision.ActorvsActor(obj.collider.component, otherObj.collider.component):
                                            obj.triggerCollided(otherObj) 

    def rayCast(self, obj):
        if self.debugLevel > 1:
            self.rays.append([obj.rayCastSystem.ray.dotList, time.time()])
        hitObjects = []
        for otherObj in self.characterObjList:
            if otherObj.collider and otherObj != obj:
                if type(otherObj.collider.component) is PhysicalEngine.Polygon:
                    for i in range(len(otherObj.collider.component.dotList)):
                        polyLine = PhysicalEngine.Line(otherObj.collider.component.dotList[i-1], otherObj.collider.component.dotList[i])
                        if self.collision.lineSegmentvsLineSegment(polyLine, obj.rayCastSystem.ray):
                            hitObjects.append(otherObj)
                            break
                else:
                    if self.collision.lineSegmentvsCircle(obj.rayCastSystem.ray, otherObj.collider.component):
                        hitObjects.append(otherObj)
        for ground in self.groundObjList:
            if ground.collider:
                if type(ground.collider.component) is PhysicalEngine.Polygon:
                    for i in range(len(ground.collider.component.dotList)):
                        polyLine = PhysicalEngine.Line(ground.collider.component.dotList[i-1], ground.collider.component.dotList[i])
                        if self.collision.lineSegmentvsLineSegment(polyLine, obj.rayCastSystem.ray):
                            hitObjects.append(ground)
                            break
                else:
                    if self.collision.lineSegmentvsCircle(obj.rayCastSystem.ray, ground.collider.component):
                        hitObjects.append(ground)
        obj.rayHit(hitObjects)
        obj.rayCastSystem.deleteRay()

    def renderCharacter(self):
        for character in self.characterObjList:#render character.(test)
            if character.renderer:# and character != player:
                a = self.handleY(character.coordinate)
                character.renderer.render(self.screen, (a[0], a[1]))#-player.coordinate[0], a[1]))

    def renderGround(self):
        # player.renderer.render(screen, handleY((500, player.coordinate[1])))
        for ground in self.groundObjList:
            if ground.renderer:
                a = self.handleY(ground.coordinate)
                ground.renderer.render(self.screen,(a[0], a[1]))#-player.coordinate[0], a[1]))

    def renderPlayerConnectedLine(self):
        dot1 = (1000, 500)
        dot2 = self.characterObjList[0].coordinate
        pygame.draw.line(self.screen, self.VIOLET, self.handleY(dot1), self.handleY(dot2), 1)
                                            
    def main(self):
        self.callUpdate()
        self.colliderCollisionCheck()
        self.triggerCollisionCheck()
        self.renderCharacter()
        self.renderGround()
        if self.debugLevel > 0:
            self.renderPlayerConnectedLine()
        if self.debugLevel > 1:
            self.renderRay()
        if self.debugLevel > 2:
            self.renderOutLine()

    def loop(self):
        done = False
        keys = [False, False]
        while not done:
            startTime = time.time()
            self.clock.tick(self.FPS)
            self.screen.fill(self.WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                    if event.key == pygame.K_LEFT:
                        keys[0] = True
                    if event.key == pygame.K_RIGHT:
                        keys[1] = True
                    if event.key == pygame.K_SPACE:
                        self.characterObjList[0].mover.moveYByAccel(10)
                    if event.key == pygame.K_DOWN:
                        self.characterObjList[0].mover.moveYByAccel(-10)
                    if event.key == pygame.K_a:
                        self.characterObjList[0].rayCastSystem.shootRayByDot(self.characterObjList[0].coordinate, (self.characterObjList[0].coordinate[0] + 300, self.characterObjList[0].coordinate[1]-300))
                    if event.key == pygame.K_d:
                        self.characterObjList[0].saySystem.say('Hi!', -1)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        keys[0] = False
                    if event.key == pygame.K_RIGHT:
                        keys[1] = False

            if keys[0]:# self.characterObjList[0] movement
                self.characterObjList[0].mover.moveXByAccel(-0.5)
            if keys[1]:
                self.characterObjList[0].mover.moveXByAccel(0.5)
            self.main()
            nowFps = 1/(time.time()-startTime)
            self.screen.blit(self.font.render(f'FPS: {round(nowFps)}', True, self.BLACK), (self.SCREEN_SIZE[0]-200, 0))
            if nowFps <60:
                self.screen.blit(self.font.render('BAD FPS!', True, self.BLACK), (self.SCREEN_SIZE[0]-100, 0))
            pygame.display.flip()
        
        pygame.quit()

    def renderOutLine(self):
        #========For debug. draw collider===============================================
        for ground in self.groundObjList:
            if ground.collider:
                if type(ground.collider.component) is PhysicalEngine.Polygon:
                    for i in range(len(ground.collider.component.dotList)):
                        dot1 = deepcopy(list(ground.collider.component.dotList[i-1]))
                        dot2 = deepcopy(list(ground.collider.component.dotList[i]))
                        dot1[0] = round(dot1[0])
                        dot2[0] = round(dot2[0])
                        dot1[1] = round(dot1[1])
                        dot2[1] = round(dot2[1])
                        pygame.draw.line(self.screen, self.BLACK, self.handleY(dot1), self.handleY(dot2), 1)
                else:
                    centerDot = deepcopy(list(ground.collider.component.centerDot))
                    centerDot[0] = round(centerDot[0])
                    centerDot[1] = round(centerDot[1])
                    pygame.draw.circle(self.screen, self.BLACK, self.handleY(centerDot), ground.collider.component.radius, 1)

        for obj in self.characterObjList:
            if obj.collider:
                if type(obj.collider.component) is PhysicalEngine.Polygon:
                    for i in range(len(obj.collider.component.dotList)):
                        dot1 = deepcopy(list(obj.collider.component.dotList[i-1]))
                        dot2 = deepcopy(list(obj.collider.component.dotList[i]))
                        dot1[0] = round(dot1[0])
                        dot2[0] = round(dot2[0])
                        dot1[1] = round(dot1[1])
                        dot2[1] = round(dot2[1])
                        pygame.draw.line(self.screen, self.BLACK, self.handleY(dot1), self.handleY(dot2), 1)
                else:
                    centerDot = deepcopy(list(obj.collider.component.centerDot))
                    centerDot[0] = int(round(centerDot[0]))
                    centerDot[1] = int(round(centerDot[1]))
                    pygame.draw.circle(self.screen, self.BLACK, self.handleY(centerDot), obj.collider.component.radius, 1)
        #========For debug. draw collider===============================================
        #========For debug, draw Trigger================================================
        for obj in self.characterObjList:
            if obj.trigger:
                if type(obj.trigger.component) is PhysicalEngine.Polygon:
                    for i in range(len(obj.trigger.component.dotList)):
                        dot1 = deepcopy(list(obj.trigger.component.dotList[i-1]))
                        dot2 = deepcopy(list(obj.trigger.component.dotList[i]))
                        dot1[0] = round(dot1[0])
                        dot2[0] = round(dot2[0])
                        dot1[1] = round(dot1[1])
                        dot2[1] = round(dot2[1])
                        pygame.draw.line(self.screen, self.RED, self.handleY(dot1), self.handleY(dot2), 1)
                else:
                    centerDot = deepcopy(list(obj.trigger.component.centerDot))
                    centerDot[0] = round(centerDot[0])
                    centerDot[1] = round(centerDot[1])
                    pygame.draw.circle(self.screen, self.RED, self.handleY(centerDot), obj.trigger.component.radius, 1)
        #========For debug, draw Trigger================================================
        #========For debug, draw AABB================================================
        for obj in self.characterObjList:#collideraabb
            if obj.collider:
                for i in range(4):
                    dot1 = deepcopy(list(obj.collider.AABB.dotList[i-1]))
                    dot2 = deepcopy(list(obj.collider.AABB.dotList[i]))
                    dot1[0] = round(dot1[0])
                    dot2[0] = round(dot2[0])
                    dot1[1] = round(dot1[1])
                    dot2[1] = round(dot2[1])
                    pygame.draw.line(self.screen, self.GREEN, self.handleY(dot1), self.handleY(dot2), 1)
        for ground in self.groundObjList:#collideraabb
            if ground.collider:
                for i in range(4):
                    dot1 = deepcopy(list(ground.collider.AABB.dotList[i-1]))
                    dot2 = deepcopy(list(ground.collider.AABB.dotList[i]))
                    dot1[0] = round(dot1[0])
                    dot2[0] = round(dot2[0])
                    dot1[1] = round(dot1[1])
                    dot2[1] = round(dot2[1])
                    pygame.draw.line(self.screen, self.GREEN, self.handleY(dot1), self.handleY(dot2), 1)
        #========For debug, draw AABB================================================
        
    def renderRay(self):
        delList = []
        for i in range(len(self.rays)):
            pygame.draw.line(self.screen, self.AQUA, self.handleY((round(self.rays[i][0][0][0]), round(self.rays[i][0][0][1]))), self.handleY((round(self.rays[i][0][1][0]), round(self.rays[i][0][1][1]))), 2)
            if time.time() - self.rays[i][1] > 1:
                delList.append(i)

        for i in range(len(delList)):
            del self.rays[delList[i] - i]
