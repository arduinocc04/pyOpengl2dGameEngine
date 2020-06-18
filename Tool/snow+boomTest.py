import pygame
import random
import time
import math

class Snow:
    def __init__(self, x, y, wind, gravity):
        '''gravity <0'''
        self.image = pygame.image.load('testSource/snow.png').convert_alpha()
        self.x = x
        self.y = y
        self.wind = wind
        self.gravity = gravity
    def render(self):
        screen.blit(self.image, dotToScreenDot(self.x, self.y))

    def move(self):
        self.x += self.wind
        self.y += self.gravity
        if self.x >= SCREEN_SIZE[0]:
            self.x -= SCREEN_SIZE[0]
        if self.y <= 0:
            self.y += SCREEN_SIZE[1]

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
        self.particleCount = 10
        self.distance = 0
        self.accel = 30
        self.startPos = False

    def startBoom(self, pos):
        self.startPos = pos
        angle = 360/self.particleCount
        for i in range(self.particleCount):
            self.particles.append(Particle(pos, angle*i))
        self.frameCount = 0
        self.distance = 0
        self.accel = 30

    def finishBoom(self):
        self.particles = []
        
    def moveParticle(self):
        for particle in self.particles:
            particle.pos = getCoordinate(particle.angle, self.distance)
            particle.pos[0] += self.startPos[0]
            particle.pos[1] += SCREEN_SIZE[1] - self.startPos[1]
        
    def idle(self):
        if self.frameCount > self.maxFrame:
            self.finishBoom()
            return
        self.frameCount += 1
        self.moveParticle()
        self.distance += self.accel
        self.accel -= 1
        
    def render(self):
        for particle in self.particles:
            pygame.draw.circle(screen, particle.color, dotToScreenDot(particle.pos[0], particle.pos[1]), particle.radius)

class BlackHole:
    def __init__(self):
        self.particles = []
        self.frameCount = 0
        self.maxFrame = 60
        self.particleCount = 30
        self.distance = 30
        self.diminish = 0
        
    def startBlackHole(self, pos):
        angle = 360/self.particleCount
        for i in range(self.particleCount):
            self.particles.append(Particle(pos, angle*i))
        self.startX = pos[0]
        self.startY = pos[1]
        
        self.diminish = 0
        self.frameCount = 0
        self.distance = 30

    def finishBlackHole(self):
        self.particles = []

    def moveParticle(self):
        for particle in self.particles:
            particle.pos = getCoordinate(particle.angle, self.distance)
            particle.pos[0] += self.startX
            particle.pos[1] += SCREEN_SIZE[1] - self.startY

    def idle(self):
        if self.frameCount > self.maxFrame:
            self.finishBlackHole()
            return
        self.frameCount += 1
        self.moveParticle()
        self.distance -= self.diminish
        self.diminish += 1
    
    def render(self):
        for particle in self.particles:
            pygame.draw.circle(screen, particle.color, dotToScreenDot(particle.pos[0], particle.pos[1]), particle.radius)

blackhole = BlackHole()
boom = Boom()

SCREEN_SIZE = (1280, 720)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

def dotToScreenDot(x,y):
    return x, SCREEN_SIZE[1]-y

done = False
snows = []
for i in range(100):
    a = random.randrange(0, SCREEN_SIZE[0])
    b = random.randrange(0, SCREEN_SIZE[0])
    snows.append(Snow(a, b, 3, -1))
BLACK = (0,0,0)
WHITE = (255, 255, 255)

FONT = 'malgungothic'
font = pygame.font.SysFont(FONT, 20)

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
            blackhole.startBlackHole((mouseX, mouseY))
            boom.startBoom((mouseX, mouseY))

    screen.fill(BLACK)

    for snow in snows:
        snow.move()
        snow.render()
    
    boom.idle()
    boom.render()
    blackhole.idle()
    blackhole.render()

    nowFps = 1/(time.time()-startTime)
    screen.blit(font.render(f'FPS: {round(nowFps)}', True, WHITE), (SCREEN_SIZE[0]-100, 0))
    pygame.display.flip()

pygame.quit()