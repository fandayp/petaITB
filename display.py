from OpenGL.GL import *
from OpenGL.GLU import *

class Display(object):

    def __init__(self):
        pass

    @classmethod
    def Clear(self, r=0, g=0,b=0,a=1):
        glClearColor(r,g,b,a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
