import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

cubeVertices = ((1,2,0),(-1,1,0),(-1,-1,0),(1,-1,0))#(x,y,z)
cubeEdges = ((0,1),(1,2),(2,3),(3,4),(4,1))
cubeQuads = ((0,1,2,3),)

def wireCube():
    glBegin(GL_LINES)
    for cubeEdge in cubeEdges:
        for cubeVertex in cubeEdge:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def solidCube():
    glBegin(GL_QUADS)
    for cubeQuad in cubeQuads:
        for cubeVertex in cubeQuad:
            glVertex3fv(cubeVertices[cubeVertex])
    glEnd()

def main():
    FPS = 60
    time = pg.time.Clock()

    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    while True:
        time.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glRotatef(1, 0, 0, 1)#angle x y z
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        solidCube()
        #wireCube()
        pg.display.flip()


if __name__ == "__main__":
    main()