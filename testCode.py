import time
import physicalEngine
import GameObject
import Components
import pygame

class TestActor(GameObject.Actor):
    def __init__(self, coordinate):
        super().__init__(coordinate)
        self.colliderSetting = 'gc'
        self.collider = physicalEngine.Circle(coordinate, 20)

        self.renderer = Components.RenderSystem(self, 'testSource/player.png')
        self.renderer.setImgSize(40, 40)
        
        self.mover = Components.MoveSystem(self)
    
    def collided(self):
        print("BAAM!")
        

if __name__ == "__main__":
    import time
    import multiprocessing
    
    FPS = 60
    SCREEN_SIZE = (1920, 1080)
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    done = False
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    groundObjList = []
    characterObjList = [TestActor((1,100)), TestActor((100, 100))]
    keys = [False, False]#leftGoKey, RightGoKey
    collision = physicalEngine.Collision()

    while not done:
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
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    keys[0] = False
                if event.key == pygame.K_RIGHT:
                    keys[1] = False

        for obj in characterObjList:#1Frame 마다 update()호출.
            obj.update()

        for obj in characterObjList:#충돌처리, 충돌하면 collided()호출.
            if obj.collider:
                if 'g' in obj.colliderSetting:
                    for ground in groundObjList:
                        if not collision.AABBvsAABB(obj.collider.AABB, ground.collider.AABB):
                            continue
                        if collision.ActorvsActor(obj, ground):
                            obj.collided()

                if 'c' in obj.colliderSetting:
                    for otherObj in characterObjList:
                        if otherObj != obj:
                            if not collision.AABBvsAABB(obj.collider.AABB, otherObj.collider.AABB):
                                continue
                            if collision.ActorvsActor(obj, otherObj):
                                obj.collided()
                                otherObj.collided()

        if keys[0]:# player movement
            characterObjList[0].mover.moveXByAccel(-0.1, 0.9)
        if keys[1]:
            characterObjList[0].mover.moveXByAccel(0.1, 0.9)
        for character in characterObjList:#render character.(test)
           # pygame.draw.circle(screen, BLACK, (int(character.coordinate[0]), int(character.coordinate[1])), character.collider.radius, 1)
           character.renderer.render(screen)
        
        for groundObj in groundObjList:
            pass
        for character in characterObjList:
            pass
        
        pygame.display.flip()

pygame.quit()