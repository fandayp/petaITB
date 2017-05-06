#!/usr/bin/env python

import sys,pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from pygame.constants import *

from OpenGL.arrays import vbo
from OpenGL.GL.shaders import compileProgram, compileShader
from ast import literal_eval as make_tuple

# import from other files in project
import ctypes

from texture import Texture
from display import Display
from shaders.vertexShader import *
from shaders.fragmentShader import *

WIDTH = 800
HEIGHT = 600
rx, ry = (0,0)
tx, ty = (0,0)
zpos = 5

class petaITB(object):
    distance = 0
    #rotation
    x_axis = 0.0
    y_axis = 0.0
    z_axis = 0.0
    vertices = []
    vertice = []

    with open("res/bangunan.txt") as f:
        z1 = 0
        z2 = 10
        lines = f.readlines()

        for i in lines:
            line = i.split('|')
            for j in line:
                if (j.find('*') == -1):
                    point = j.split(',')
                    vertices.append(make_tuple('(%d,%s,%s)' % (int(point[0])-270, z1, point[1])))
            for j in line:
                if (j.find('*') == -1):
                    point = j.split(',')
                    vertices.append(make_tuple('(%d,%s,%s)' % (int(point[0])-270, z2, point[1])))

            vertice.append(tuple(vertices))

            del vertices[:]

    #vertices = ((0,0,55), (7,0,055), (7,0,037), (0,0,037), (0,10,055), (7,10,055), (7,10,037), (0,10,037))
    

    vertices = [
    #      x,  y,  z, x_tex, y_tex, nor_x, nor_y, nor_z
        [ -0.85, -1, 1, 0, 0, 0, 0, 1],
        [ 0.85, -1, 1, 1, 0, 0, 0, 1],
        [ 0.85, -1, -1, 1, 1, 0, 0, 1],
        [ -0.85, -1, -1, 0, 1, 0, 0, 1],

        [ 0.031, -1, -0.0757042*2, 0, 0, 0, 0, 1],#
        [ 0.195, -1, -0.0757042*2, 1, 0, 0, 0, 1],#

        [ 0.195, -1, -0.04049*2, 1, 1, 0, 0, 1],
        [ 0.031, -1, -0.04049*2, 0, 1, 0, 0, 1],

        [ 0.031, -0.92, -0.0757042*2, 0, 1, 0, 0, 1],#
        [ 0.195, -0.92, -0.0757042*2, 1, 1, 0, 0, 1],#

        [ 0.195, -0.92, -0.04049*2, 0, 1, 0, 0, 1],
        [ 0.031, -0.92, -0.04049*2, 1, 1, 0, 0, 1],
    ]


    indices = [
        # use depan texture
        [0, 1, 2, 3],

        #depan belakang
        [4, 5, 9, 8],
        [7, 6, 10, 11],

        #samping
        [5, 6, 10, 9],
        [4, 7, 11, 8],
        #atas
        [8, 9, 10, 11],
    ]

    texcoord = ((0,0),(1,0),(1,1),(0,1))
    #-------------------------------------
    def __init__(self):

        self.coordinates = [0,0,0] # buat apa?

        # initialize texture
        self.texEnum = ('depan', 'belakang', 'samping1', 'samping2')
        self.tex = [
            Texture("res/jalan.jpg"),
            Texture("res/lab-7-1.jpg"),
            Texture("res/lab7-samping.jpg"),
        ]


        # initialize shader
        try:
            self.shader = compileProgram(
                compileShader( VERTEX_SHADER, GL_VERTEX_SHADER ),
                compileShader( FRAGMENT_SHADER, GL_FRAGMENT_SHADER )
            )
        except RuntimeError as err:
            sys.stderr.write( err.args[0] )
            sys.exit( 1 )

        self.vertices = vbo.VBO(np.array(self.vertices, dtype='f'))
        self.indices = vbo.VBO(np.array(self.indices, dtype='uint32'),target='GL_ELEMENT_ARRAY_BUFFER')

        for uniform in (
            'Global_ambient',
            'Light_ambient',
            'Light_diffuse',
            'Light_location',
            'Material_ambient',
            'Material_diffuse',
        ):
            location = glGetUniformLocation( self.shader, uniform )
            if location in ( None, -1 ):
                print ('Warning, no uniform: %s'%( uniform ))
            setattr( self, uniform+ '_loc', location )

        for attribute in (
            'Vertex_position',
            'Vertex_texCoord',
            'Vertex_normal',
        ):
            location = glGetAttribLocation(self.shader, attribute)
            if location in ( None, -1 ):
                print ('Warning, no attribute: %s' %( attribute ))
            setattr( self, attribute + '_loc', location )

    def initMesh(self):
        glUniform4f( self.Global_ambient_loc, .9,.05,.05,.1 )
        glUniform4f( self.Light_ambient_loc, .2,.2,.2, 1.0 )
        glUniform4f( self.Light_diffuse_loc, 1,1,1,1 )

        glUniform3f( self.Light_location_loc, 2,2,10 )
        glUniform4f( self.Material_ambient_loc, .2,.2,.2, 1.0 )
        glUniform4f( self.Material_diffuse_loc, 1,1,1, 1 )

        stride = 8*4 # x y z x_tex y_tex r g b * sizeof(float)
        glEnableVertexAttribArray( self.Vertex_position_loc ) # 0
        glEnableVertexAttribArray( self.Vertex_texCoord_loc ) # 1
        glEnableVertexAttribArray( self.Vertex_normal_loc ) # 2

        # bind the vertex attribute location
        glVertexAttribPointer(self.Vertex_position_loc, 3, GL_FLOAT, False, stride, self.vertices)
        glVertexAttribPointer(self.Vertex_texCoord_loc, 2, GL_FLOAT, False, stride, self.vertices + 12)
        glVertexAttribPointer(self.Vertex_normal_loc  , 3, GL_FLOAT, False, stride, self.vertices + 20)

    def draw(self):
        '''
        render the scene geometry
        '''
        glUseProgram(self.shader)

        try:
            self.vertices.bind()
            self.indices.bind()
            try:
                self.initMesh()
                self.tex[0].Bind(0)
                glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, ctypes.c_void_p(0))

                self.tex[2].Bind(0)
                glDrawElements(GL_QUADS, 8, GL_UNSIGNED_INT, ctypes.c_void_p(16))

                self.tex[1].Bind(0)
                glDrawElements(GL_QUADS, 12, GL_UNSIGNED_INT, ctypes.c_void_p(48))
                """self.tex[1].Bind(0)
                glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, ctypes.c_void_p(12))

                self.tex[2].Bind(0)
                glDrawElements(GL_TRIANGLES, 9, GL_UNSIGNED_INT, ctypes.c_void_p(24))

                self.tex[3].Bind(0)
                glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, ctypes.c_void_p(60))"""

            finally:
                self.vertices.unbind()
                self.indices.unbind()

                glDisableVertexAttribArray( self.Vertex_position_loc ) # 0
                glDisableVertexAttribArray( self.Vertex_texCoord_loc ) # 1
                glDisableVertexAttribArray( self.Vertex_normal_loc ) # 2
        finally:
            glUseProgram(0)

    def render_scene(self):
        Display.Clear()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        global ry, rx, tx, ty, zpos
        glTranslate(tx/20., ty/20., - zpos)
        glRotate(ry, 1, 0, 0)
        glRotate(rx, 0, 1, 0)
        #  glTranslatef(0, 1,-60)
        #glRotatef(30,30,60,0)
        #  glRotatef(self.y_axis,0,1,0)

        self.draw()

        self.y_axis = self.y_axis - 1


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH , HEIGHT),pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Xiaomi")
    clock = pygame.time.Clock()
    done = False

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(0.5, 1.0 * WIDTH/HEIGHT, 0.1, 1000.0)
    glEnable(GL_DEPTH_TEST)
    global rx, ry, ty, tx, zpos
    
    rotate = move = False
	
    xiaomi = petaITB()
    #----------- Main Program Loop -------------------------------------
    while not done:
        # --- Main event loop
        for e in pygame.event.get(): # User did something
            if e.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4: zpos = max(1, zpos-1)
                elif e.button == 5: zpos += 1
                elif e.button == 1: rotate = True
                elif e.button == 3: move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1: rotate = False
                elif e.button == 3: move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j
        clock.tick(30)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # RENDER OBJECT
        xiaomi.render_scene()

        pygame.display.flip()
    
    pygame.quit()



if __name__ == '__main__':
    main()
