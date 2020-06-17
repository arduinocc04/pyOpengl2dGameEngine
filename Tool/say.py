import pygame
import time

SCREEN_SIZE = (1280, 720)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

BLACK = (0,0,0)
WHITE = (255, 255, 255)

FONT = 'malgungothic'
FONT_SIZE = 20
font = pygame.font.SysFont(FONT, FONT_SIZE)


done = False

FPS = 60
clock = pygame.time.Clock()
script = input('말할 것 입력')
show = True
while not done:
    startTime = time.time()
    clock.tick(FPS)
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
    if show:    
        mouseX, mouseY = pygame.mouse.get_pos()
        pygame.draw.rect(screen, BLACK, (mouseX, mouseY, FONT_SIZE*len(script), (len(script)//20 + 1)*(FONT_SIZE+5)))
        pygame.draw.polygon(screen, BLACK, [[(mouseX+FONT_SIZE*len(script)//5) - 5, mouseY+(len(script)//20 + 1)*FONT_SIZE+5], [(mouseX+FONT_SIZE*len(script)//5), mouseY+(len(script)//20 + 1)*FONT_SIZE + 10], [(mouseX+FONT_SIZE*len(script)//5) + 5, mouseY+(len(script)//20 + 1)*FONT_SIZE+5]])
        screen.blit(font.render(script, True, WHITE), (mouseX, mouseY))
    
    nowFps = 1/(time.time() - startTime)
    screen.blit(font.render(f'FPS: {round(nowFps)}', True, BLACK), (SCREEN_SIZE[0]-100, 0))
    pygame.display.flip()