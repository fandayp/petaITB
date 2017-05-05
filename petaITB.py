#!/usr/bin/env python

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

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

class Xiaomi(object):
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

    #vertices = ((0,0,055), (7,0,055), (7,0,037), (0,0,037), (0,10,055), (7,10,055), (7,10,037), (0,10,037))

    indices = [
        # use depan texture
        [4, 0, 3, 7],

        # use belakang texture
        [1, 5, 6, 2],

        # use samping1 texture
        [0, 1, 2, 3],
        [4, 7, 6, 5],
        [2, 6, 7, 3],

        # use samping2 texture
        [0, 4, 5, 1],

        #(9,10,11,12),
        #(13,16,15,14),
        #(9,13,14,10),
        #(10,14,15,11),
        #(11,15,16,12),
        #(13,9,12,16),
    ]

    texcoord = ((0,0),(1,0),(1,1),(0,1))
    #-------------------------------------
    def __init__(self):

        self.coordinates = [0,0,0] # buat apa?

        # initialize texture
        self.texEnum = ('depan', 'belakang', 'samping1', 'samping2')
        self.tex = [
            Texture("res/depan.jpg"),
            Texture("res/belakang.jpg"),
            Texture("res/samping.jpg"),
            Texture("res/samping2.jpg"),
        ]


        # initialize shader
        try:
            self.shader = compileProgram(
                compileShader( VERTEX_SHADER, GL_VERTEX_SHADER ),
                compileShader( FRAGMENT_SHADER, GL_FRAGMENT_SHADER )
            )
        except RuntimeError, err:
            sys.stderr.write( err.args[0] )
            sys.exit( 1 )

        self.vertices = vbo.VBO(array(vertices, 'f'))
        self.indices = vbo.VBO(array(indices, 'uint32'),target='GL_ELEMENT_ARRAY_BUFFER')

        for attribute in (
            'Vertex_position',
            'Vertex_texCoord',
            'Vertex_normal',
        ):
            location = glGetAttribLocation(self.shader, attribute)
            if location in ( None, -1 ):
                print 'Warning, no attribute: %s'%( attribute )
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
                self.tex[0].Bind(0)
                glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, ctypes.c_void_p(0))

                self.tex[1].Bind(0)
                glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, ctypes.c_void_p(16))

                self.tex[2].Bind(0)
                glDrawElements(GL_QUADS, 12, GL_UNSIGNED_INT, ctypes.c_void_p(32))

                self.tex[3].Bind(0)
                glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, ctypes.c_void_p(80))

            finally:
                self.vertices.unbind()
                self.indices.unbind()
        finally:
            glUseProgram(0)

    def render_scene(self):
        Display.clear()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslatef(0,0,-60)

        glRotatef(self.y_axis,0,1,0)

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
    gluPerspective(45 , 1.0 * WIDTH/HEIGHT ,0.1,200.0)
    glEnable(GL_DEPTH_TEST)

    xiaomi = Xiaomi()
    #----------- Main Program Loop -------------------------------------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

        xiaomi.render_scene()

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()



if __name__ == '__main__':
	main()
