import time
import PhysicalEngine
import GameObject
import Components
import pygame
'''
characterObjList[0]이 무조건 Player
'''

def getSquaredDistanceBetweenDot(dot1, dot2):
    return (dot1[0]-dot2[0])**2 + (dot1[1]-dot2[1])**2

class TestActor(GameObject.Actor):
    def __init__(self, coordinate):
        super().__init__(coordinate)
        self.colliderSetting = 'gc'
        self.collider = PhysicalEngine.Circle(coordinate, 20)

        self.renderer = Components.RenderSystem(self)
        self.renderer.setImage('testSource/player.png')
        self.renderer.setImgSize(40, 40)
        
        self.soundSystem = Components.SoundSystem('testSource/ballade4.ogg')
        self.soundSystem.diminishVolumePercentPer100px = 0.2
        self.soundSystem.playSound(-1)

        self.healthSystem = Components.HealthSystem(500, 500)

        self.mover = Components.MoveSystem(self)
        self.mover.friction = 0.9

        self.trigger = Components.Trigger(PhysicalEngine.Circle(coordinate, 100))
        self.triggerSetting = 'c'
    
    def collided(self):
        pass

    def update(self):
        self.mover.idle()
        self.soundSystem.setVolumeByDistance(getSquaredDistanceBetweenDot(self.coordinate, characterObjList[1].coordinate))

    
    def triggerCollided(self, collidedObj):
        pass

class TestActor1(GameObject.Actor):
    def __init__(self, coordinate):
        super().__init__(coordinate)
        self.colliderSetting = 'gc'
        self.collider = PhysicalEngine.Circle(coordinate, 20)

        self.renderer = Components.RenderSystem(self)
        self.renderer.setImage('testSource/player.png')
        self.renderer.setImgSize(40, 40)
        #self.AI = Components.AI(self)
        
        self.mover = Components.MoveSystem(self)
        self.mover.friction = 0.9
        self.healthSystem = Components.HealthSystem(100, 100)

    def update(self):
        self.mover.idle()
       # self.AI.chase(characterObjList[0], 0.5, 30)
    
    def collided(self):
        pass

class TestActor2(GameObject.Actor):
    def __init__(self, coordinate):
        super().__init__(coordinate)
       # self.colliderSetting = 'gc'
       # self.collider = PhysicalEngine.Circle(coordinate, 5)

        self.renderer = Components.RenderSystem(self)
        self.renderer.setImage('testSource/player.png')
        self.renderer.setImgSize(10, 10)
        

        self.mover = Components.MoveSystem(self)
        self.mover.friction = 0.9

        self.trigger = Components.Trigger(PhysicalEngine.Circle(coordinate, 100))
        self.triggerSetting = 'c'
    
    def collided(self):
        pass

    def update(self):
        self.mover.moveXByAccel(0.3)
        self.mover.idle()
    
    def triggerCollided(self, collidedObj):
        pass

if __name__ == "__main__":
    FPS = 60
    SCREEN_SIZE = (1920, 1080)
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    done = False
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    groundObjList = []
    characterObjList = [TestActor((1,100)), TestActor1((100, 100))]
    for i in range(100):
        characterObjList.append(TestActor2((i,i)))
    keys = [False, False]#leftGoKey, RightGoKey
    collision = PhysicalEngine.Collision()
    player = characterObjList[0]

    while not done:
        startTime = time.time()
        #clock.tick(FPS)
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys[0] = False
                if event.key == pygame.K_RIGHT:
                    keys[1] = False

        for obj in characterObjList:
            obj.update()#call update() per frame

        #=======================collision Detection=============================================================
            if obj.collider:#collision detection.if collided, call collided().(characterObject)
                if 'g' in obj.colliderSetting:
                    for ground in groundObjList:
                        if collision.AABBvsAABB(obj.collider.AABB, ground.collider.AABB):
                            if collision.ActorvsActor(obj.collider, ground.collider):
                                obj.collided()

                if 'c' in obj.colliderSetting:
                    for otherObj in characterObjList:
                        if otherObj != obj and otherObj.collider:
                            if collision.AABBvsAABB(obj.collider.AABB, otherObj.collider.AABB):
                                if collision.ActorvsActor(obj.collider, otherObj.collider):
                                    obj.collided()
                                    otherObj.collided()

            if obj.trigger:#trigger collision detection
                if 'p' in obj.triggerSetting:
                    if not obj is player and player.collider:
                        if collision.AABBvsAABB(obj.trigger.AABB, player.collider.AABB):
                            if collision.ActorvsActor(obj.trigger.component, player.collider):
                                obj.triggerCollided(player)
                        
                if 'c' in obj.triggerSetting:
                    for otherObj in characterObjList:
                        if otherObj != obj and otherObj.collider:
                            if collision.AABBvsAABB(obj.trigger.AABB, otherObj.collider.AABB):
                                if collision.ActorvsActor(obj.trigger.component, otherObj.collider):
                                    obj.triggerCollided(otherObj)
        #=======================collision Detection=============================================================                    

        if keys[0]:# player movement
            player.mover.moveXByAccel(-0.5)
        if keys[1]:
            player.mover.moveXByAccel(0.5)

        for character in characterObjList:#render character.(test)
            try:
                character.renderer.render(screen)
            except AttributeError:
                pass

        pygame.display.flip()
        print('FPS: ', 1.0/(time.time()-startTime))

pygame.quit()