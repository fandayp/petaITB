#!/usr/bin/env python

import pygame
import numpy as np
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

    vertOnly = [
        [-0.85, -1, 1],
        [ 0.85, -1, 1],
        [ 0.85, -1, -1],
        [-0.85, -1, -1],

        # Bangunan Labtek VII
        [ 0.062, -1, -0.1514084],#
        [ 0.390, -1, -0.1514084],#
        [ 0.390, -1, -0.08098],
        [ 0.062, -1, -0.08098],
        [ 0.062, -0.95, -0.1514084],#
        [ 0.390, -0.95, -0.1514084],#
        [ 0.390, -0.95, -0.08098],
        [ 0.062, -0.95, -0.08098],

        # Bangunan Labtek VII
        [-0.380282, -1, -0.147887],
        [-0.052817, -1, -0.147887],
        [-0.052817, -1, -0.073944],
        [-0.380282, -1, -0.073944],
        [-0.380282, -0.950000, -0.147887],
        [-0.052817, -0.950000, -0.147887],
        [-0.052817, -0.950000, -0.073944],
        [-0.380282, -0.950000, -0.073944],

        # Bangunan Labtek V
        [-0.345070, -1, 0.014085],
        [-0.042254, -1, 0.014085],
        [-0.042254, -1, 0.098592],
        [-0.345070, -1, 0.098592],
        [-0.345070, -0.950000, 0.014085],
        [-0.042254, -0.950000, 0.014085],
        [-0.042254, -0.950000, 0.098592],
        [-0.345070, -0.950000, 0.098592],

        #Bangungan Labtek VIII
        [0.049296, -1, -0.007042],
        [0.369718, -1, -0.007042],
        [0.369718, -1, 0.098592],
        [0.049296, -1, 0.098592],
        [0.049296, -0.950000, -0.007042],
        [0.369718, -0.950000, -0.007042],
        [0.369718, -0.950000, 0.098592],
        [0.049296, -0.950000, 0.098592],

        #Bangungan Lab UMH
        [0.454225, -1, -0.172535],
        [0.658451, -1, -0.172535],
        [0.658451, -1, -0.102113],
        [0.454225, -1, -0.102113],
        [0.454225, -0.980000, -0.172535],
        [0.658451, -0.980000, -0.172535],
        [0.658451, -0.980000, -0.102113],
        [0.454225, -0.980000, -0.102113],

        #Bangungan GKU Timur
        [0.531690, -1, -0.095070],
        [0.721831, -1, -0.095070],
        [0.721831, -1, 0.000000],
        [0.531690, -1, 0.000000],
        [0.531690, -0.950000, -0.095070],
        [0.721831, -0.950000, -0.095070],
        [0.721831, -0.950000, 0.000000],
        [0.531690, -0.950000, 0.000000],

        #Bangungan Doping
        [0.464789, -1, 0.066901],
        [0.577465, -1, 0.066901],
        [0.577465, -1, 0.133803],
        [0.464789, -1, 0.133803],
        [0.464789, -0.950000, 0.066901],
        [0.577465, -0.950000, 0.066901],
        [0.577465, -0.950000, 0.133803],
        [0.464789, -0.950000, 0.133803],

        #M Tek Geodesi
        [0.644366, -1, 0.010563],
        [0.711268, -1, 0.010563],
        [0.711268, -1, 0.088028],
        [0.644366, -1, 0.088028],
        [0.644366, -0.990000, 0.010563],
        [0.711268, -0.990000, 0.010563],
        [0.711268, -0.990000, 0.088028],
        [0.644366, -0.990000, 0.088028],

        #M.S & T Jil Raya (?)
        [0.654930, -1, 0.098592],
        [0.707746, -1, 0.098592],
        [0.707746, -1, 0.169014],
        [0.654930, -1, 0.169014],
        [0.654930, -0.990000, 0.098592],
        [0.707746, -0.990000, 0.098592],
        [0.707746, -0.990000, 0.169014],
        [0.654930, -0.990000, 0.169014],
    ]

    texOnly = [
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
    ]

    norOnly = [
        [0, 0, 1],
    ]

    vert = [
        # ALAS
        vertOnly[0] + texOnly[0] + norOnly[0],
        vertOnly[1] + texOnly[1] + norOnly[0],
        vertOnly[2] + texOnly[2] + norOnly[0],
        vertOnly[3] + texOnly[3] + norOnly[0],
    ]

    ind = [
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

    def makeCuboid(self, startIndex, startNor = 0):
        vert_ans = [
            # depan belakang texture
            self.vertOnly[startIndex + 0] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 1] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 5] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 4] + self.texOnly[3] + self.norOnly[startNor],

            self.vertOnly[startIndex + 3] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 2] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 6] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 7] + self.texOnly[3] + self.norOnly[startNor],

            # samping texture
            self.vertOnly[startIndex + 1] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 2] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 6] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 5] + self.texOnly[3] + self.norOnly[startNor],

            self.vertOnly[startIndex + 0] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 3] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 7] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 4] + self.texOnly[3] + self.norOnly[startNor],

            # atas, texture same with samping 
            self.vertOnly[startIndex + 4] + self.texOnly[0] + self.norOnly[startNor],
            self.vertOnly[startIndex + 5] + self.texOnly[1] + self.norOnly[startNor],
            self.vertOnly[startIndex + 6] + self.texOnly[2] + self.norOnly[startNor],
            self.vertOnly[startIndex + 7] + self.texOnly[3] + self.norOnly[startNor],
        ]
        return vert_ans

    # masukkan base dari bangunan disini
    def initVertices(self):
        #self.vert.extend(self.makeCuboid(4)) # Bangunan Labtek VII
        for i in range(0, 9):
            self.vert.extend(self.makeCuboid(i*8+4))

    #-------------------------------------
    def __init__(self):

        # initialize texture
        self.texEnum = ('jalan','roof','lab7-kirikanan', 'lab7-depanbelakang')
        self.tex = [
            Texture("res/jalan.jpg"),
            Texture("res/roof.jpg"),

            Texture("res/lab7-kanankiri.jpg"),
            Texture("res/lab7-depanbelakang.jpg"),

            Texture("res/gkutimur-kanankiri.jpg"),
            Texture("res/gkutimur-depanbelakang.jpg"),

            Texture("res/doping-kanankiri.jpg"),
            Texture("res/doping-depanbelakang.jpg"),

            Texture("res/geodesi-kanankiri.jpg"),
            Texture("res/geodesi-depanbelakang.jpg"),

            Texture("res/ms-kanankiri.jpg"),
            Texture("res/ms-depanbelakang.jpg"),
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

        self.initVertices()

        self.vertices = vbo.VBO(np.array(self.vert, dtype='f'))
        self.indices = vbo.VBO(np.array(self.ind, dtype='uint32'),target='GL_ELEMENT_ARRAY_BUFFER')

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
                glDrawArrays(GL_QUADS, 0, 4)
                #glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, ctypes.c_void_p(0))

                cuboid_count = (self.vert.__len__() - 4) / 20
                #khusus labtek tengah texture sama
                for i in range(0, 5):
                    self.tex[3].Bind(0) #depan belakang
                    glDrawArrays(GL_QUADS, i * 20 + 4, 8)
                   
                    self.tex[2].Bind(0) #kanan kiri
                    glDrawArrays(GL_QUADS, i * 20 + 12, 8)

                    self.tex[1].Bind(0) #atap
                    glDrawArrays(GL_QUADS, i * 20 + 20, 4)

                #bangunan berikutnya
                for i in range(5, int(cuboid_count)):
                    self.tex[(i-3)*2 + 1].Bind(0) #depan belakang
                    glDrawArrays(GL_QUADS, i * 20 + 4, 8)

                    self.tex[(i-3)*2].Bind(0) #kanan kiri
                    glDrawArrays(GL_QUADS, i * 20 + 12, 8)

                    self.tex[1].Bind(0) #atap
                    glDrawArrays(GL_QUADS, i * 20 + 20, 4)

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

        glTranslatef(0, 1,-60)
        glRotatef(self.y_axis, -2, -2, 0)

        self.draw()

        self.y_axis = self.y_axis - 1

def main():
    pygame.init()
    pygame.display.set_mode((WIDTH , HEIGHT),pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("petaITB")
    clock = pygame.time.Clock()
    done = False

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(2, 1.0 * WIDTH/HEIGHT, 0.01, 1000.0)
    glEnable(GL_DEPTH_TEST)

    petaitb = petaITB()
    #----------- Main Program Loop -------------------------------------
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

        petaitb.render_scene()

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()



if __name__ == '__main__':
    main()
