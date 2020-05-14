import math
import pygame
import numpy as np

pygame.init()
SCREEN_SIZE = (1920, 1080)

basicLineDistance = 20
done = False
shapeList = []

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT = 'malgungothic'
font = pygame.font.SysFont(FONT, 20)
helpText = ['ctrl+P:Making Polygon', 'ctrl+C:Making Circle', 'ctrl+q:Finish draw shape', 'ctrl+F:Finish and extract.',
            'ctrl+d:Delete Shape', 'ctrl+M:move Screen', 'ctrl+r:rotateLastModifedShape.', 'arrowTo rotate(+-1), ctrl+arrow to rotate(+-10)', 
            'Set mode and click Coordinate.', 'esc or alt+F4: Close']
isGround = input('is ground or actor. ground->y, actor ->n')
if isGround == 'n':
    isGround = False
actorName = input('what is your actor\'s name?')
actorCoordinate = input('where to place your actor input like x y. ex) 23 100').split()
actorCoordinate[0], actorCoordinate[1] = int(actorCoordinate[0]), int(actorCoordinate[1])
needRenderer = input('Do you need render?  y/n')
if needRenderer == 'n':
    needRenderer = False
if needRenderer:
    actorImage = input('Input your image directory. ex) testSource/image.png')
if not isGround:
    colliderSetting = input('what is your collider setting? g->ground only, c-> character only, gc->both. g/c/gc')
    needTrigger = input('Do you need trigger? y/n')
    if needTrigger == 'n':
        needTrigger = False
    if needTrigger:
        triggerSetting = input('hwat is your trigger setting? p->player only, c-> character only(except player) pc->both p/c/pc')



def renderTextsGroup(coordinate, textList, fontSize, color, backgroundColor, antialias=True):
    maxTextLen = 0
    for text in textList:
        if len(text) > maxTextLen:
            maxTextLen = len(text)

    pygame.draw.rect(screen, backgroundColor, [coordinate[0], coordinate[1], round(maxTextLen*fontSize*0.5),(len(textList) + 1)*fontSize])#draw background
    for i in range(len(textList)):
        text = font.render(textList[i], antialias, color)
        screen.blit(text, (coordinate[0], coordinate[1] + i * fontSize))


def returnClickedCoordinate():
    mouseX, mouseY = pygame.mouse.get_pos()
    screenDot = (screenCoordinate[0] // lineDistance, screenCoordinate[1] // lineDistance)
    dotX = round(mouseX / lineDistance) + screenDot[0]
    dotY = round((SCREEN_SIZE[1] - mouseY) / lineDistance) + screenDot[1]
    return (dotX, dotY)


def dotToScreenDot(dot):
    screenDot = (screenCoordinate[0] // lineDistance, screenCoordinate[1] // lineDistance)
    return int(round((dot[0] - screenDot[0]) * lineDistance)), int(round(SCREEN_SIZE[1] - (dot[1] - screenDot[1]) * lineDistance))


def drawDotAndCoordinate(coordinate, color, antialias=True):
    text = coordiFont.render(f'({coordinate[0]/lineDistance + screenCoordinate[0]//lineDistance}, {(SCREEN_SIZE[1]-coordinate[1]+screenCoordinate[1])/lineDistance})', antialias, color)
    screen.blit(text, (coordinate[0]+2, coordinate[1]+2))
    pygame.draw.circle(screen, BLACK, coordinate, 3)
    

class Poly:
    def __init__(self):
        self.dotList = []
        self.angle = 0

    def appendNewDot(self, coordinate):
        self.dotList.append(coordinate)
    
    def isDotInDotList(self, dot):
        if dot in self.dotList:
            return True
        return False

    def extract(self):
        dotList = ''
        for dot in self.dotList:
            dotList += str(dot) + ' '
        dotList = dotList[:-1]
        return f'physicalEngine.Polygon({dotList}, {self.angle})'
    
    def rotate(self, angle):
        xList = []
        yList = []
        for dot in self.dotList:
            xList.append(dot[0])
            yList.append(dot[1])
        self.centeroidDot = ((min(xList)+max(xList))/2, (min(yList)+max(yList))/2)

        self.angle += angle
        if self.angle<0:
            self.angle += 360
        if self.angle>360:
            self.angle -= 360
        if angle == 90:
            expression = np.array([[0, -1], [1, 0]])
        elif angle == 180:
            expression = np.array([[-1, 0], [0, -2]])
        elif angle == 270:
            expression = np.array([[0, 1], [-1, 0]])
        else:
            angle = math.radians(angle)
            expression = np.array([[math.cos(angle), -math.sin(angle)],[math.sin(angle), math.cos(angle)]])

        for i in range(len(self.dotList)):
            self.dotList[i] = np.dot(expression, (np.array(self.dotList[i])-np.array(self.centeroidDot)).T) + np.array(self.centeroidDot)

class Circle:
    def __init__(self):
        self.centerDot = -1
        self.radius = -1

    def setCenterDot(self, centerDot):
        self.centerDot = centerDot

    def calcRadius(self, otherDot):
        radius = math.sqrt((self.centerDot[0] - otherDot[0])**2 + (self.centerDot[1] - otherDot[1])**2)
        self.radius = radius

    def extract(self):
        return f'physicalEngine.Circle({str(self.centerDot)}, {self.radius})'


mode = 'Move'
ctrlPressed = False
altPressed = False
shapeList = []
screenCoordinate = [0, 0]
moving = False

coordiFont = pygame.font.SysFont(FONT, 10)
zoom = 1
lineDistance = basicLineDistance
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
actorImage = pygame.image.load(actorImage).convert_alpha()
while not done:
    #clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            dot = returnClickedCoordinate()

            if mode == 'MakingPoly':
                if nowShape.isDotInDotList(dot):
                    mode = 'QUIT'
                    shapeList.append(nowShape)
                else:
                    nowShape.appendNewDot(dot)
                        
            elif mode == 'MakingCircle':
                if nowShape.centerDot == -1:
                    nowShape.setCenterDot(dot)
                elif nowShape.radius == -1:
                    nowShape.calcRadius(dot)
                    shapeList.append(nowShape)
                    mode = 'QUIT'

            elif mode == 'Move':
                prevCoordinate = pygame.mouse.get_pos()
                moving = True

            elif mode == 'Delete':
                for i in range(len(shapeList)):
                    if type(shapeList[i]) is Poly:
                        for shapeDot in shapeList[i].dotList:
                            if abs(dot[0]-shapeDot[0])<=0.5 and abs(dot[1]-shapeDot[1])<=0.5:
                                del shapeList[i]
                                break
                    else:
                        if dot == shapeList[i].centerDot:
                            del shapeList[i]
                            break

        if event.type == pygame.MOUSEBUTTONUP:
            if mode == 'Move':
                nowCoordinate = pygame.mouse.get_pos()
                xToMove = prevCoordinate[0] - nowCoordinate[0]
                yToMove = nowCoordinate[1] - prevCoordinate[1]

                screenCoordinate[0] += xToMove
                screenCoordinate[1] += yToMove

                if screenCoordinate[0] < 0:
                    screenCoordinate[0] = 0
                if screenCoordinate[1] < 0:
                    screenCoordinate[1] = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                ctrlPressed = True
            if event.key == pygame.K_LALT:
                altPressed = True
            if event.key == pygame.K_RIGHT and mode == 'Rotate':
                if type(shapeList[-1]) is Poly:
                    if ctrlPressed:
                        shapeList[-1].rotate(-10)
                    else:
                        shapeList[-1].rotate(-1)
                else:
                    pass
            if event.key == pygame.K_LEFT and mode == 'Rotate':
                if type(shapeList[-1]) is Poly:
                    if ctrlPressed:
                        shapeList[-1].rotate(10)
                    else:
                        shapeList[-1].rotate(1)
                else:
                    pass
            if event.key == pygame.K_UP:
                zoom += 0.5
                lineDistance = round(zoom*basicLineDistance)
            if event.key == pygame.K_DOWN:
                temporaryZoomLev = zoom-0.5
                if temporaryZoomLev<=0:
                    screen.blit(font.render('Cannnot Zoom!', True, (255, 0, 0)), (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))
                    temporaryZoomLev = zoom
                else:
                    zoom = temporaryZoomLev
                lineDistance = round(zoom*basicLineDistance)
            if ctrlPressed:
                if event.key == pygame.K_p:
                    mode = 'MakingPoly'
                    nowShape = Poly()
                if event.key == pygame.K_c:
                    mode = 'MakingCircle'
                    nowShape = Circle()
                if event.key == pygame.K_d:
                    mode = 'Delete'
                if event.key == pygame.K_m:
                    mode = 'Move'
                if event.key == pygame.K_r:
                    mode = "Rotate"
                if event.key == pygame.K_q:
                    shapeList.append(nowShape)
                    mode = 'QUIT'
                if event.key == pygame.K_f:
                    mode = 'EXTRACT'
                    with open('result.txt', 'w+t', encoding='utf8') as f:
                        for shape in shapeList:
                            f.write(shape.extract() + '\n')
                    done = True
            if (altPressed and event.key == pygame.K_F4) or event.key == pygame.K_ESCAPE:
                done = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrlPressed = False
            if event.key == pygame.K_LALT:
                altPressed = False

    screen.fill(WHITE)

    for i in range(SCREEN_SIZE[1]//lineDistance):  # draw x line
        pygame.draw.line(screen, BLACK, [0, i*lineDistance], [SCREEN_SIZE[0], i*lineDistance], 1)

    for i in range(SCREEN_SIZE[0]//lineDistance):  # draw y line
        pygame.draw.line(screen, BLACK, [i*lineDistance, 0], [i*lineDistance, SCREEN_SIZE[1]], 1)

    for i in range(SCREEN_SIZE[0]//lineDistance):  # draw x value.
        screen.blit(coordiFont.render(str(screenCoordinate[0]//lineDistance + i), True, BLACK), (SCREEN_SIZE[0]%lineDistance + lineDistance*i, SCREEN_SIZE[1]//2))

    for i in range(SCREEN_SIZE[1]//lineDistance):  # draw y value
        screen.blit(coordiFont.render(str(screenCoordinate[1]//lineDistance + i), True, BLACK), (SCREEN_SIZE[0]//2,SCREEN_SIZE[1] - (SCREEN_SIZE[1]%lineDistance + lineDistance*i + 12)))  # 12는 y좌표 살짝 위에 띄우기 위해 넣은 값.

    if mode == 'MakingPoly':
        for i in range(len(nowShape.dotList)):
            if len(nowShape.dotList) > 1:
                pygame.draw.line(screen, BLACK,
                                 dotToScreenDot(nowShape.dotList[i-1]),
                                 dotToScreenDot(nowShape.dotList[i]), 2)
            drawDotAndCoordinate(dotToScreenDot(nowShape.dotList[i]), BLACK)
    elif mode == 'MakingCircle':
        if nowShape.centerDot != -1:
            drawDotAndCoordinate(dotToScreenDot(nowShape.centerDot), BLACK)
            if nowShape.radius != -1:
                pygame.draw.circle(screen, BLACK,
                                   dotToScreenDot(nowShape.centerDot),
                                   round(nowShape.radius * lineDistance), 1)
    for shape in shapeList:
        if type(shape) is Poly:
            for i in range(len(shape.dotList)):
                pygame.draw.line(screen, BLACK,
                                 dotToScreenDot(shape.dotList[i-1]),
                                 dotToScreenDot(shape.dotList[i]), 2)
                drawDotAndCoordinate(dotToScreenDot(shape.dotList[i]), BLACK)
        else:
            drawDotAndCoordinate(dotToScreenDot(shape.centerDot), BLACK)
            pygame.draw.circle(screen, BLACK,
                               dotToScreenDot(shape.centerDot),
                               round(shape.radius*lineDistance), 1)

    renderTextsGroup((0, 0), helpText, 20, BLACK, WHITE)
    screen.blit(font.render(f'MODE: {mode}', True, BLACK, WHITE), (SCREEN_SIZE[0] - 200, 0))#show mode
    screen.blit(actorImage, actorCoordinate)#render actor's image
    pygame.display.flip()

pygame.quit()
