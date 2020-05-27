import pygame
import time
import math
import random

SCREEN_SIZE = (1280, 720)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0,0,0)
WHITE = (255, 255, 255)

FONT = 'malgungothic'
font = pygame.font.SysFont(FONT, 20)

done = False

class Particle:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        self.radius = random.randrange(5, 10)

def getCoordinate(angle, distance):
    angle = math.pi*angle/180
    return [round(distance*math.cos(angle)), round(distance*math.sin(angle))]

def dotToScreenDot(x,y):
    return x, SCREEN_SIZE[1]-y

class Boom:
    def __init__(self):
        self.particles = []
        self.frameCount = 0
        self.maxFrame = 60
        self.particleCount = 30
        self.distance = 60
        

    def startBoom(self, pos):
        angle = 360/self.particleCount
        for i in range(self.particleCount):
            self.particles.append(Particle(pos, angle*i))
        self.startX = pos[0]
        self.startY = pos[1]

    def finishBoom(self):
        self.frameCount = 0
        self.particles = []
        self.distance = 60

    def moveParticle(self):
        for particle in self.particles:
            particle.pos = getCoordinate(particle.angle, self.distance)
            particle.pos[0] += self.startX
            particle.pos[1] += SCREEN_SIZE[1] - self.startY

    def idle(self):
        if self.frameCount > self.maxFrame:
            self.finishBoom()
            return
        self.frameCount += 1
        self.moveParticle()
        self.distance -= 1
    
    def render(self):
        for particle in self.particles:
            pygame.draw.circle(screen, particle.color, dotToScreenDot(particle.pos[0], particle.pos[1]), particle.radius)

boom = Boom()
clock = pygame.time.Clock()
FPS = 60
while not done:
    startTime = time.time()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            boom.startBoom((mouseX, mouseY))
    
    screen.fill(WHITE)
    boom.idle()
    boom.render()

    nowFps = 1/(time.time() - startTime)
    screen.blit(font.render(f'FPS: {round(nowFps)}', True, BLACK), (SCREEN_SIZE[0]-100, 0))
    pygame.display.flip()
pygame.quit()