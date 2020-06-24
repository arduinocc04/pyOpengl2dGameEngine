import time
import PhysicalEngine
import GameObject
import Components
import pygame
from copy import deepcopy
import Scene

class TestActor(GameObject.Actor):
    def __init__(self, coordinate):
        super().__init__(coordinate)
        self.colliderSetting = 'gc'
        #self.collider = Components.Collider(PhysicalEngine.Circle(coordinate, 20))
        self.collider = Components.Collider(PhysicalEngine.Polygon([coordinate, (coordinate[0]+40, coordinate[1]), (coordinate[0]+40, coordinate[1]-40), (coordinate[0], coordinate[1]-40)]))

        self.renderer = Components.RenderSystem(self)
        self.renderer.setImage('testSource/player.png')
        self.renderer.setImgSize(40, 40)
        
        #self.soundSystem = Components.SoundSystem('testSource/ballade4.ogg')
       # self.soundSystem.diminishVolumePercentPer100px = 0.2
       # self.soundSystem.playSound(-1)

        self.healthSystem = Components.HealthSystem(500, 500)

        self.mover = Components.MoveSystem(self)
        self.mover.friction = 0.9
        self.mover.airResistance = 1

        # self.trigger = Components.Trigger(PhysicalEngine.Circle(coordinate, 100))
       # self.trigger = Components.Trigger(PhysicalEngine.Polygon([coordinate, (coordinate[0]+40, coordinate[1]), (coordinate[0]+40, coordinate[1]-40), (coordinate[0], coordinate[1]-40)]))
        self.triggerSetting = 'c'

        self.rigidPhysicsSystem = Components.RigidPhysicsSystem(self.mover)

        self.rayCastSystem = Components.RayCastSystem(scene, self)

        self.saySystem = Components.SaySystem('malgungothic', 20, screen, self)
    
    def collided(self, otherObj):
        if otherObj.type:#ground->type = True, Actor->type = False
            self.rigidPhysicsSystem.groundUp()

    def update(self):
        self.rigidPhysicsSystem.gravity(-0.1)
        self.mover.rotate(10)
        self.mover.idle()
        self.saySystem.idle()
        #self.soundSystem.diminishVolumeByDistance()

    def rayHit(self, hitObjs):
        print(hitObjs)

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
            self.rigidPhysicsSystem.groundUp()

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
    pygame.init()
    def handleY(dot):
        return dot[0], SCREEN_SIZE[1]-dot[1]

    scene = Scene.Scene(screen, SCREEN_SIZE, FPS, debugLevel=3)
    scene.addCharacterObj(TestActor(handleY([1,100])))
    scene.addCharacterObj(TestActor1(handleY([100, 100])))
    for i in range(40):
        scene.addGroundObj(TestGround(handleY([i*40, 1000])))

    scene.loop()

    