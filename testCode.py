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

def getSquaredDistanceBetweenDot(dot1, dot2):
    return (dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2

def handleY(dot):
    return dot[0], SCREEN_SIZE[1]-dot[1]

class TestActor(GameObject.Actor):
    def __init__(self, coordinate):
        super().__init__(coordinate)
        self.colliderSetting = 'gc'
        #self.collider = Components.Collider(PhysicalEngine.Circle(coordinate, 20))
        self.collider = Components.Collider(PhysicalEngine.Polygon([coordinate, (coordinate[0]+40, coordinate[1]), (coordinate[0]+40, coordinate[1]-40), (coordinate[0], coordinate[1]-40)]))

        self.renderer = Components.RenderSystem(self)
        self.renderer.setImage('testSource/player.png')
        self.renderer.setImgSize(40, 40)
        
        self.soundSystem = Components.SoundSystem('testSource/ballade4.ogg')
        self.soundSystem.diminishVolumePercentPer100px = 0.2
        self.soundSystem.playSound(-1)

        self.healthSystem = Components.HealthSystem(500, 500)

        self.mover = Components.MoveSystem(self)
        self.mover.friction = 0.9
        self.mover.airResistance = 1

        # self.trigger = Components.Trigger(PhysicalEngine.Circle(coordinate, 100))
       # self.trigger = Components.Trigger(PhysicalEngine.Polygon([coordinate, (coordinate[0]+40, coordinate[1]), (coordinate[0]+40, coordinate[1]-40), (coordinate[0], coordinate[1]-40)]))
        self.triggerSetting = 'c'

        self.rigidPhysicsSystem = Components.RigidPhysicsSystem(self.mover)
    
    def collided(self, otherObj):
        if otherObj.type:#ground->type = True, Actor->type = False
            self.mover.speedY = 0
            self.mover.moveYByAccel(0.3)
            self.mover.idle()
    def update(self):
        self.rigidPhysicsSystem.gravity(-0.1)
        self.mover.idle()
        self.soundSystem.setVolumeByDistance(getSquaredDistanceBetweenDot(self.coordinate, characterObjList[1].coordinate))

class TestActor1(GameObject.Actor):
    def __init__(self, coordinate):
        super().__init__(coordinate)
        self.colliderSetting = 'g'
        self.collider = Components.Collider(PhysicalEngine.Circle(coordinate, 20))

        self.renderer = Components.RenderSystem(self)
        self.renderer.setImage('testSource/player.png')
        self.renderer.setImgSize(40, 40)
        # self.AI = Components.AI(self)
        
        self.mover = Components.MoveSystem(self)
        self.mover.friction = 0.9
        self.healthSystem = Components.HealthSystem(100, 100)

        self.rigidPhysicsSystem = Components.RigidPhysicsSystem(self.mover)

    def update(self):
        self.rigidPhysicsSystem.gravity(-0.1)
        self.mover.idle()
        # self.AI.chase(characterObjList[0], 0.5, 30)
    
    def collided(self, otherObj):
        if otherObj.type:
            self.mover.speedY = 0
            self.mover.moveYByAccel(1)
            self.mover.idle()

class TestGround(GameObject.Ground):
    def __init__(self, coordinate):
        super().__init__(coordinate)
        self.collider = Components.Collider(PhysicalEngine.Polygon([coordinate, (coordinate[0]+40, coordinate[1]), (coordinate[0]+40, coordinate[1]-40), (coordinate[0], coordinate[1]-40)]))

        self.renderer = Components.RenderSystem(self)
        self.renderer.setImage('testSource/player.png')
        self.renderer.setImgSize(40, 40)
    
    def update(self):
        self.mover.moveXByAccel(0.3)
        self.mover.idle()

if __name__ == "__main__":
    FPS = 60
    SCREEN_SIZE = (1920, 1080)
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    done = False
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    groundObjList = []
    characterObjList = [TestActor(handleY([1,100])), TestActor1(handleY([100, 100]))]
    for i in range(40):
        groundObjList.append(TestGround(handleY([i*40,1000])))
    keys = [False, False]#leftGoKey, RightGoKey
    collision = PhysicalEngine.Collision()
    player = characterObjList[0]
    pygame.init()
    FONT = 'malgungothic'
    font = pygame.font.SysFont(FONT, 20)
    screenAABB = PhysicalEngine.AABB((0,0), SCREEN_SIZE)

    while not done:
        startTime = time.time()
        clock.tick(FPS)
        screen.fill(WHITE)

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
                    player.mover.moveYByAccel(10)
                if event.key == pygame.K_DOWN:
                    player.mover.moveYByAccel(-10)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys[0] = False
                if event.key == pygame.K_RIGHT:
                    keys[1] = False

        for obj in characterObjList:
            obj.update()#call update() per frame

            if collision.AABBvsAABB(screenAABB, obj.collider.AABB):
                if obj.collider:#collision detection.if collided, call collided().(characterObject)
                    if 'g' in obj.colliderSetting:
                        for ground in groundObjList:
                            if collision.AABBvsAABB(obj.collider.AABB, ground.collider.AABB):
                                if collision.isAABBCompAABB(obj.collider.AABB, ground.collider.AABB):
                                    obj.collided(ground)
                                    screen.blit(font.render('Collided!', True, BLACK), (0, 0))
                                else:
                                    if collision.ActorvsActor(obj.collider.component, ground.collider.component):
                                        obj.collided(ground)
                                        screen.blit(font.render('Collided!', True, BLACK), (0, 0))

                    if 'c' in obj.colliderSetting:
                        for otherObj in characterObjList:
                            if otherObj != obj and otherObj.collider and otherObj.allowCharacterColliding:
                                if collision.AABBvsAABB(obj.collider.AABB, otherObj.collider.AABB):
                                    if collision.isAABBCompAABB(obj.collider.AABB, otherObj.collider.AABB):
                                        obj.collided(otherObj)
                                        otherObj.collided(obj)
                                        screen.blit(font.render('Collided!', True, BLACK), (0,0))
                                    else:
                                        if collision.ActorvsActor(obj.collider.component, otherObj.collider.component):
                                            obj.collided(otherObj)
                                            otherObj.collided(obj)
                                            screen.blit(font.render('Collided!', True, BLACK), (0,0))

                if obj.trigger:#trigger collision detection
                    if 'p' in obj.triggerSetting:
                        if not obj is player and player.collider:
                            if collision.AABBvsAABB(obj.trigger.AABB, player.collider.AABB):
                                if collision.isAABBCompAABB(obj.trigger.AABB, player.collider.AABB):
                                    obj.triggerCollided(player)
                                else:
                                    if collision.ActorvsActor(obj.trigger.component, player.collider.component):
                                        obj.triggerCollided(player)

                    if 'c' in obj.triggerSetting:
                        for otherObj in characterObjList:
                            if otherObj != obj and otherObj.collider:
                                if collision.AABBvsAABB(obj.trigger.AABB, otherObj.collider.AABB):
                                    if collision.isAABBCompAABB(obj.trigger.AABB, otherObj.collider.AABB):
                                        obj.triggerCollided(otherObj)
                                    else:
                                        if collision.ActorvsActor(obj.collider.component, otherObj.collider.component):
                                            obj.triggerCollided(otherObj)        

        if keys[0]:# player movement
            player.mover.moveXByAccel(-0.5)
        if keys[1]:
            player.mover.moveXByAccel(0.5)

        for character in characterObjList:#render character.(test)
            if character.renderer:# and character != player:
                a = handleY(character.coordinate)
                character.renderer.render(screen, (a[0], a[1]))#-player.coordinate[0], a[1]))
       # player.renderer.render(screen, handleY((500, player.coordinate[1])))
        for ground in groundObjList:
            if ground.renderer:
                a = handleY(ground.coordinate)
                ground.renderer.render(screen,(a[0], a[1]))#-player.coordinate[0], a[1]))
        """
        #========For debug. draw collider===============================================
        for ground in groundObjList:
            if ground.collider:
                if type(ground.collider.component) is PhysicalEngine.Polygon:
                    for i in range(len(ground.collider.component.dotList)):
                        dot1 = deepcopy(list(ground.collider.component.dotList[i-1]))
                        dot2 = deepcopy(list(ground.collider.component.dotList[i]))
                        dot1[0] = round(dot1[0])
                        dot2[0] = round(dot2[0])
                        dot1[1] = round(dot1[1])
                        dot2[1] = round(dot2[1])
                        pygame.draw.line(screen, BLACK, handleY(dot1), handleY(dot2), 1)
                else:
                    centerDot = deepcopy(list(ground.collider.component.centerDot))
                    centerDot[0] = round(centerDot[0])
                    centerDot[1] = round(centerDot[1])
                    pygame.draw.circle(screen, BLACK, handleY(centerDot), ground.collider.component.radius, 1)

        for obj in characterObjList:
            if obj.collider:
                if type(obj.collider.component) is PhysicalEngine.Polygon:
                    for i in range(len(obj.collider.component.dotList)):
                        dot1 = deepcopy(list(obj.collider.component.dotList[i-1]))
                        dot2 = deepcopy(list(obj.collider.component.dotList[i]))
                        dot1[0] = round(dot1[0])
                        dot2[0] = round(dot2[0])
                        dot1[1] = round(dot1[1])
                        dot2[1] = round(dot2[1])
                        pygame.draw.line(screen, BLACK, handleY(dot1), handleY(dot2), 1)
                else:
                    centerDot = deepcopy(list(obj.collider.component.centerDot))
                    centerDot[0] = int(round(centerDot[0]))
                    centerDot[1] = int(round(centerDot[1]))
                    pygame.draw.circle(screen, BLACK, handleY(centerDot), obj.collider.component.radius, 1)
        #========For debug. draw collider===============================================
        #========For debug, draw Trigger================================================
        for obj in characterObjList:
            if obj.trigger:
                if type(obj.trigger.component) is PhysicalEngine.Polygon:
                    for i in range(len(obj.trigger.component.dotList)):
                        dot1 = deepcopy(list(obj.trigger.component.dotList[i-1]))
                        dot2 = deepcopy(list(obj.trigger.component.dotList[i]))
                        dot1[0] = round(dot1[0])
                        dot2[0] = round(dot2[0])
                        dot1[1] = round(dot1[1])
                        dot2[1] = round(dot2[1])
                        pygame.draw.line(screen, (255, 0, 0), handleY(dot1), handleY(dot2), 1)
                else:
                    centerDot = deepcopy(list(obj.trigger.component.centerDot))
                    centerDot[0] = round(centerDot[0])
                    centerDot[1] = round(centerDot[1])
                    pygame.draw.circle(screen, (255, 0, 0), handleY(centerDot), obj.trigger.component.radius, 1)
        #========For debug, draw Trigger================================================
        #========For debug, draw AABB================================================
        for obj in characterObjList:#collideraabb
            if obj.collider:
                for i in range(4):
                    dot1 = deepcopy(list(obj.collider.AABB.dotList[i-1]))
                    dot2 = deepcopy(list(obj.collider.AABB.dotList[i]))
                    dot1[0] = round(dot1[0])
                    dot2[0] = round(dot2[0])
                    dot1[1] = round(dot1[1])
                    dot2[1] = round(dot2[1])
                    pygame.draw.line(screen, (0, 255, 0), handleY(dot1), handleY(dot2), 1)
        for ground in groundObjList:#collideraabb
            if ground.collider:
                for i in range(4):
                    dot1 = deepcopy(list(ground.collider.AABB.dotList[i-1]))
                    dot2 = deepcopy(list(ground.collider.AABB.dotList[i]))
                    dot1[0] = round(dot1[0])
                    dot2[0] = round(dot2[0])
                    dot1[1] = round(dot1[1])
                    dot2[1] = round(dot2[1])
                    pygame.draw.line(screen, (0, 255, 0), handleY(dot1), handleY(dot2), 1)
        #========For debug, draw AABB================================================
        """
        nowFps = 1.0/(time.time()-startTime)
        screen.blit(font.render(f'FPS: {round(nowFps)}', True, BLACK), (SCREEN_SIZE[0]-200, 0))
        if nowFps <60:
            screen.blit(font.render('BAD FPS!', True, BLACK), (SCREEN_SIZE[0]-100, 0))
        pygame.display.flip()

pygame.quit()