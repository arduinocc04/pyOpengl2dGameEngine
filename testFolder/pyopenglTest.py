from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def initFun():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)

def square():
    glBegin(GL_QUADS)
    glVertex2f(100, 100)
    glVertex2f(200, 100)
    glVertex2f(200, 200)
    glVertex2f(100, 200)
    glEnd()

def displayFun():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glScalef(1.0, 1.0, 0.0)#x y z
    glutWireCube(1.0)

    glFlush()


def reshapeFun(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode(GL_MODELVIEW)

def timer(FPS):
    glutTimerFunc(FPS, timer, 5)

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

if __name__ == '__main__':
    glutInit()
    timer(1000//60)
    glutInitWindowSize(1280, 720)
    glutCreateWindow(b"Cube")
    gluPerspective(45, (1280 / 720), 0.1, 50.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(solidCube)
    glutDisplayFunc(displayFun)
    glutReshapeFunc(reshapeFun)

    initFun()

    glutMainLoop()