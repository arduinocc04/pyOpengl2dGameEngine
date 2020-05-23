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
helpText = ['ctrl+P:Making Polygon', 'ctrl+C:Making Circle', 'ctrl+q:Finish draw shape', 'ctrl+F:Finish and extract.', 'ctrl+h: toggle helpMessage', 'ctrl+y: make rectangle that surround image',
            'ctrl+d:Delete Shape', 'ctrl+M:move Screen', 'ctrl+r:rotateLastModifedShape.', 'arrowTo rotate(+-1), ctrl+arrow to rotate(+-10)', 'ctrl+v: toggle show real size in game',
            'upArrow, downArrow to zoom', 'firstInputShape->collider, second->trigger(if need)', 'Set mode and click Coordinate.', 'esc or alt+F4: Close']
for text in helpText:
    print(text)
#==================================config==========================================
isGround = input('is ground or actor. ground->y, actor ->n>>>  ')
if isGround == 'n':
    isGround = False
actorName = input('what is your actor\'s name?>>>  ')
actorCoordinate = input('where to place your actor input like x y. ex) 23 100>>>  ').split()
actorCoordinate[0], actorCoordinate[1] = int(actorCoordinate[0]), int(actorCoordinate[1])
needRenderer = input('Do you need render?  y/n>>>  ')
if needRenderer == 'n':
    needRenderer = False
if needRenderer:
    actorImageDir = input('Input your image directory. ex) testSource/image.png>>>  ')
needTrigger = False
if not isGround:
    colliderSetting = input('what is your collider setting? g->ground only, c-> character only, gc->both. g/c/gc>>>>  ')
    needTrigger = input('Do you need trigger? y/n>>>  ')
    if needTrigger == 'n':
        needTrigger = False
    if needTrigger:
        triggerSetting = input('hwat is your trigger setting? p->player only, c-> character only(except player) pc->both p/c/pc>>>  ')
#===================================config===============================================


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
        self.basicDotList = []

    def appendNewDot(self, coordinate):
        self.dotList.append(coordinate)
        self.basicDotList.append(coordinate)
    
    def isDotInDotList(self, dot):
        if dot in self.dotList:
            return True
        return False

    def extract(self):
        dotList = ''
        for dot in self.basicDotList:
            dotList += f'({dot[0]}, {dot[1]}), '
        dotList = dotList[:-2]
        return f'PhysicalEngine.Polygon({dotList})'
    
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
        return f'PhysicalEngine.Circle({str(self.centerDot)}, {self.radius})'


mode = 'Move'
ctrlPressed = False
altPressed = False
shapeList = []
screenCoordinate = actorCoordinate
moving = False

coordiFont = pygame.font.SysFont(FONT, 10)
zoom = 1
lineDistance = basicLineDistance
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
if needRenderer:
    actorBasicImage = pygame.image.load(actorImageDir).convert_alpha()
    imageWidth, imageHeight = actorBasicImage.get_rect().size
    actorImage = pygame.transform.scale(actorBasicImage, (imageWidth*lineDistance, imageHeight*lineDistance))# in game: + 1px means +1 x. but in this tool: +lineDistancepx means +1 x
showHelper = True
showRealSize = False
angle = 0
while not done:
    #clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            dot = returnClickedCoordinate()

            if mode == 'MakingPoly':
                if nowShape.isDotInDotList(dot):
                    shapeList.append(nowShape)
                    mode = 'QUIT'
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
                        angle -= 10
                        shapeList[-1].rotate(-10)
                        actorImage = pygame.transform.rotate(actorBasicImage, angle)
                    else:
                        angle -= 1
                        shapeList[-1].rotate(-1)
                        actorImage = pygame.transform.rotate(actorBasicImage, angle)
                else:
                    pass
            if event.key == pygame.K_LEFT and mode == 'Rotate':
                if type(shapeList[-1]) is Poly:
                    if ctrlPressed:
                        angle += 10
                        shapeList[-1].rotate(10)
                        actorImage = pygame.transform.rotate(actorBasicImage, 10)
                    else:
                        angle += 1
                        shapeList[-1].rotate(1)
                        actorImage = pygame.transform.rotate(actorBasicImage, 1)
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
                    mode = 'QUIT'
                    shapeList.append(nowShape)
                if event.key == pygame.K_f:
                    mode = 'EXTRACT'
                if event.key == pygame.K_y:
                    nowShape = Poly()
                    nowShape.appendNewDot(actorCoordinate)
                    nowShape.appendNewDot((actorCoordinate[0], actorCoordinate[1]-imageHeight))
                    nowShape.appendNewDot((actorCoordinate[0]+imageWidth, actorCoordinate[1]-imageHeight))
                    nowShape.appendNewDot((actorCoordinate[0]+imageWidth, actorCoordinate[1]))
                    shapeList.append(nowShape)
                    mode = 'QUIT'
                if event.key == pygame.K_h:
                    showHelper = not(showHelper)
                if event.key == pygame.K_v:
                    showRealSize = not showRealSize
                    if showRealSize:
                        prevLineDistance = lineDistance
                        actorImage = pygame.transform.scale(actorBasicImage, (imageWidth, imageHeight))
                        lineDistance = 1
                    else:
                        lineDistance = prevLineDistance
                        actorImage = pygame.transform.scale(actorBasicImage, (imageWidth*lineDistance, imageHeight*lineDistance))
            if (altPressed and event.key == pygame.K_F4) or event.key == pygame.K_ESCAPE:
                done = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                ctrlPressed = False
            if event.key == pygame.K_LALT:
                altPressed = False

    #========================draw coordinate system============================================
    screen.fill(WHITE)
    for i in range(SCREEN_SIZE[1]//lineDistance):  # draw x line
        pygame.draw.line(screen, BLACK, [0, i*lineDistance], [SCREEN_SIZE[0], i*lineDistance], 1)

    for i in range(SCREEN_SIZE[0]//lineDistance):  # draw y line
        pygame.draw.line(screen, BLACK, [i*lineDistance, 0], [i*lineDistance, SCREEN_SIZE[1]], 1)

    for i in range(SCREEN_SIZE[0]//lineDistance):  # draw x value.
        screen.blit(coordiFont.render(str(screenCoordinate[0]//lineDistance + i), True, BLACK), (SCREEN_SIZE[0]%lineDistance + lineDistance*i, SCREEN_SIZE[1]//2))

    for i in range(SCREEN_SIZE[1]//lineDistance):  # draw y value
        screen.blit(coordiFont.render(str(screenCoordinate[1]//lineDistance + i), True, BLACK), (SCREEN_SIZE[0]//2,SCREEN_SIZE[1] - (SCREEN_SIZE[1]%lineDistance + lineDistance*i + 12)))  # 12는 y좌표 살짝 위에 띄우기 위해 넣은 값.
    
    if showRealSize:#del grid, coordinate text.
        screen.fill(WHITE)
    #===================================draw coordinate system==========================
    
    #============================render=================================================
    if needRenderer:
        screen.blit(actorImage, dotToScreenDot(actorCoordinate))#render actor's image
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
    if showHelper:
        renderTextsGroup((0, 0), helpText, 20, BLACK, WHITE)
    screen.blit(font.render(f'MODE: {mode}', True, BLACK, WHITE), (SCREEN_SIZE[0] - 200, 0))#show mode
    #=====================================================================================

    if mode == 'EXTRACT':
        with open('result.txt', 'w+t', encoding='utf8') as f:
            if isGround:
                parent = 'GameObject.Ground'
            else:
                parent = 'GameObject.Actor'
            f.write(f'class {actorName}({parent}):\n')
            f.write(f'    def __init__(self, coordinate):\n')
            f.write(f'        super().__init__(self, coordinate)\n\n')
            f.write(f'        self.collider = Components.Collider({shapeList[0].extract()})\n')
            if not isGround:
                f.write(f'        self.colliderSetting = \'{colliderSetting}\'\n')
            if needRenderer:
                f.write(f'        self.renderer = Components.RenderSystem(self)\n')
                f.write(f'        self.renderer.setImage = \'{actorImageDir}\'\n\n')
            if needTrigger:
                f.write(f'        self.triggerSetting = \'{triggerSetting}\'\n')
                f.write(f'        self.trigger = Components.Trigger({shapeList[1].extract()})\n\n')
            if shapeList[0].angle != 0:
                f.write(f'        self.mover = Components.MoveSystem(self)\n')
                f.write(f'        self.mover.rotate({shapeList[0].angle})')

        done = True
    
    pygame.display.flip()

pygame.quit()
