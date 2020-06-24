import pygame
import time

SCREEN_SIZE = (1280, 720)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0,0,0)
WHITE = (255, 255, 255)

FONT = 'malgungothic'
font = pygame.font.SysFont(FONT, 20)

done = False
FPS = 60
clock = pygame.time.Clock()

def getDotvsDotDistanceSquared(dot1, dot2):
    return (dot1[0] - dot2[0])**2 + (dot1[1] - dot2[1])**2

class Slider:
    def __init__(self, lineStartDot, width):
        self.line = (lineStartDot, (lineStartDot[0] + width, lineStartDot[1]))
        self.value = 0
        self.circleCenterDot = lineStartDot[:]
        self.width = width
        self.circleRad = 10
    
    def getPercent(self):
        '''
        0<=return<=1
        '''
        return abs(self.line[0][0] - self.circleCenterDot[0])/self.width

    def moveCircle(self, coordinate):
        if self.line[0][0] > coordinate[0]:
            x = self.line[0][0]
        elif self.line[1][0] < coordinate[0]:
            x = self.line[1][0]
        else:
            x = coordinate[0]
        self.circleCenterDot = (x, self.line[0][1])

    def render(self):
        pygame.draw.line(screen, BLACK, self.line[0], self.line[1], 5)
        pygame.draw.circle(screen, BLACK, self.circleCenterDot, self.circleRad)

slider1 = Slider((300, 540), 400)
clicked = False
while not done:
    startTime = time.time()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            if slider1.line[0][0] - slider1.circleRad <= mouseX and slider1.line[1][0] + slider1.circleRad >= mouseX and slider1.line[0][1] + slider1.circleRad >= mouseY and slider1.line[0][1] - slider1.circleRad <= mouseY:
                clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False

    if clicked:
        mouseX, mouseY = pygame.mouse.get_pos()
        slider1.moveCircle((mouseX, mouseY))

    screen.fill(WHITE)
    slider1.render()
    screen.blit(font.render(f'{slider1.getPercent()*100}%', True, BLACK), (1000, 200))
    nowFps = time.time()-startTime
    if nowFps != 0:
        nowFps = 1.0/nowFps
    else:
        nowFps = 'INFINITY!'
    screen.blit(font.render(f'{nowFps}', True, BLACK), (1000, 0))
    pygame.display.flip()

pygame.quit()