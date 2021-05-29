# Freeglut failed to open display (Python, MacOS)
# https://stackoverflow.com/questions/61022231/freeglut-failed-to-open-display-python-macos

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

rotate = [33, 40, 20]

def display():
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -4.5)
    glColor3f(0.8, 0.2, 0.1)
    glRotatef(rotate[0], 1, 0.0, 0)
    glRotatef(rotate[1], 0, 1, 0)
    glRotatef(rotate[2], 0, 0, 1)
    glScalef(1, 1, 1)
    glutSolidTeapot(1)
    glFlush()
    glutSwapBuffers()

def reshapeFunc(x, y):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, x / y, 0.5, 20.0)
    glViewport(0, 0, x, y)

def idleFunc():
    rotate[1] += 0.01
    display()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(400, 350)
glutCreateWindow(b"OpenGL Window")
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
glClearColor(0.0, 0.0, 0.0, 0.0)
glutDisplayFunc(display)
glutReshapeFunc(reshapeFunc)
glutIdleFunc(idleFunc)
glutMainLoop()