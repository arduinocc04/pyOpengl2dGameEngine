import math
import pygame

pygame.init()

SCREEN_SIZE = (1920, 1080)
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 60

lineDistance = 40
done = False
shapeList = []

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont('malgungothic', 20)
helpText = ['ctrl+P:Making Polygon', 'ctrl+C:Making Circle', 'ctrl+q:Finish draw shape', 'ctrl+F:Finish and extract.',
            'ctrl+d:Delete Shape', 'ctrl+M:move Screen', 'Set mode and click Coordinate.', 'esc or alt+F4: Close']

def renderMultiLineText(screen, coordinate, textList, fontSize, color, backgroundColor, antialias=True):
    maxTextLen = 0
    for text in textList:
        if len(text) > maxTextLen:
            maxTextLen = len(text)

    pygame.draw.rect(screen, backgroundColor, [coordinate[0], coordinate[1], round(maxTextLen*fontSize*0.5),
                                               (len(textList) + 1)*fontSize])  # background
    for i in range(len(textList)):
        text = font.render(textList[i], antialias, color)
        screen.blit(text, (coordinate[0], coordinate[1] + i * fontSize))


def returnClickedCoordinate(SCREEN_SIZE, screenCoordinate, lineDistance):
    mouseX, mouseY = pygame.mouse.get_pos()
    screenDot = (screenCoordinate[0] // lineDistance, screenCoordinate[1] // lineDistance)
    dotX = round(mouseX / lineDistance) + screenDot[0]
    dotY = round((SCREEN_SIZE[1] - mouseY) / lineDistance) + screenDot[1]
    # dotY = SCREEN_SIZE[1] - (round(mouseY/lineDistance)-screenDot[1])*lineDistance
    return (dotX, dotY)


def dotToScreenDot(dot, lineDistance, SCREEN_SIZE, screenCoordinate):
    screenDot = (screenCoordinate[0] // lineDistance, screenCoordinate[1] // lineDistance)
    return ((dot[0] - screenDot[0]) * lineDistance,
            (SCREEN_SIZE[1] - (dot[1] - screenDot[1]) * lineDistance))  # +screenDot[1]*lineDistance)
    # return (dot[0]*lineDistance, SCREEN_SIZE[1] - dot[1]*lineDistance)


def drawDot(screen, coordinate, color):
    pygame.draw.circle(screen, BLACK, coordinate, 3)


class Poly:
    def __init__(self):
        self.dotList = []

    def appendNewDot(self, coordinate):
        self.dotList.append(coordinate)

    def extract(self):
        dotList = ''
        for dot in self.dotList:
            dotList += str(dot) + ' '
        dotList[:-1]
        return f'physicalEngine.Polygon({dotList}, MASS)'


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
        return f'physicalEngine.Circle({str(self.centerDot)}, {self.radius}, MASS)'


mode = 'Move'
ctrlPressed = False
altPressed = False
shapeList = []
screenCoordinate = [0, 0]
moving = False

coordiFont = pygame.font.SysFont('malgungothic', 10)
while not done:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            dot = returnClickedCoordinate(SCREEN_SIZE, screenCoordinate, lineDistance)

            if mode == 'MakingPoly':
                nowShape.appendNewDot(dot)
                if len(nowShape.dotList) > 1:
                    if nowShape.dotList[0] == nowShape.dotList[-1]:
                        del nowShape.dotList[-1]
                        mode = 'QUIT'
                        shapeList.append(nowShape)
            elif mode == 'MakingCircle':
                if nowShape.centerDot == -1:
                    nowShape.setCenterDot(dot)
                elif nowShape.radius == -1:
                    nowShape.calcRadius(dot)
                    mode = 'QUIT'
                    shapeList.append(nowShape)
            elif mode == 'Move':
                prevCoordinate = pygame.mouse.get_pos()
                moving = True
            elif mode == 'Delete':
                for i in range(len(shapeList)):
                    if type(shapeList[i]) is Poly:
                        if dot in shapeList[i].dotList:
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
        screen.blit(coordiFont.render(str(screenCoordinate[0]//lineDistance + i), True, BLACK),
                    (SCREEN_SIZE[0]%lineDistance + lineDistance*i, SCREEN_SIZE[1]//2))

    for i in range(SCREEN_SIZE[1]//lineDistance):  # draw y value
        screen.blit(coordiFont.render(str(screenCoordinate[1]//lineDistance + i), True, BLACK), (SCREEN_SIZE[0]//2,SCREEN_SIZE[1] - (SCREEN_SIZE[1]%lineDistance + lineDistance*i + 12)))  # 12는 y좌표 살짝 위에 띄우기 위해 넣은 값.

    if mode == 'MakingPoly':
        for i in range(len(nowShape.dotList)):
            if len(nowShape.dotList) > 1:
                pygame.draw.line(screen, BLACK,
                                 dotToScreenDot(nowShape.dotList[i-1], lineDistance, SCREEN_SIZE, screenCoordinate),
                                 dotToScreenDot(nowShape.dotList[i], lineDistance, SCREEN_SIZE, screenCoordinate), 2)
            drawDot(screen, dotToScreenDot(nowShape.dotList[i], lineDistance, SCREEN_SIZE, screenCoordinate), BLACK)
    elif mode == 'MakingCircle':
        if nowShape.centerDot != -1:
            drawDot(screen, dotToScreenDot(nowShape.centerDot, lineDistance, SCREEN_SIZE, screenCoordinate), BLACK)
            if nowShape.radius != -1:
                pygame.draw.circle(screen, BLACK,
                                   dotToScreenDot(nowShape.centerDot, lineDistance, SCREEN_SIZE, screenCoordinate),
                                   round(nowShape.radius * lineDistance), 1)
    for shape in shapeList:
        if type(shape) is Poly:
            for i in range(len(shape.dotList)):
                pygame.draw.line(screen, BLACK,
                                 dotToScreenDot(shape.dotList[i-1], lineDistance, SCREEN_SIZE, screenCoordinate),
                                 dotToScreenDot(shape.dotList[i], lineDistance, SCREEN_SIZE, screenCoordinate), 2)
                drawDot(screen, dotToScreenDot(shape.dotList[i], lineDistance, SCREEN_SIZE, screenCoordinate), BLACK)
        else:
            drawDot(screen, dotToScreenDot(shape.centerDot, lineDistance, SCREEN_SIZE, screenCoordinate), BLACK)
            pygame.draw.circle(screen, BLACK,
                               dotToScreenDot(shape.centerDot, lineDistance, SCREEN_SIZE, screenCoordinate),
                               round(shape.radius*lineDistance), 1)

    renderMultiLineText(screen, (0, 0), helpText, 20, BLACK, WHITE)
    screen.blit(font.render(f'MODE: {mode}', True, BLACK, WHITE), (SCREEN_SIZE[0] - 200, 0))

    pygame.display.flip()

pygame.quit()
