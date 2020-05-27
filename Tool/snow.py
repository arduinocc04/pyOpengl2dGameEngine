import pygame
import random
import time

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

    screen.fill(BLACK)

    for snow in snows:
        snow.move()
        snow.render()

    nowFps = 1/(time.time()-startTime)
    screen.blit(font.render(f'FPS: {round(nowFps)}', True, WHITE), (SCREEN_SIZE[0]-100, 0))
    pygame.display.flip()

pygame.quit()