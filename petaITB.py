#!/usr/bin/env python

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from ast import literal_eval as make_tuple

from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()

# import from other files in project
from texture import Texture
from shaders.vertexShader import *
from shaders.fragmentShader import *

WIDTH = 640
HEIGHT = 480

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

    faces = (
        (1,2,3,4),
        (5,8,7,6),
        (1,5,6,2),
        (2,6,7,3),
        (3,7,8,4),
        (5,1,4,8)
        #(9,10,11,12),
        #(13,16,15,14),
        #(9,13,14,10),
        #(10,14,15,11),
        #(11,15,16,12),
        #(13,9,12,16),
        )
    texcoord = ((0,0),(1,0),(1,1),(0,1))
    #-------------------------------------
    def __init__(self):
        self.coordinates = [0,0,0]
        self.depan_id = self.load_texture("res/depan.jpg")
        self.belakang_id = self.load_texture("res/belakang.jpg")
        self.samping1_id = self.load_texture("res/samping.jpg")
        self.samping2_id = self.load_texture("res/samping2.jpg")

    def load_texture(self,filename):
        textureSurface = pygame.image.load(filename)
        textureData = pygame.image.tostring(textureSurface,"RGBA",1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,textureData)
        return ID

    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glTranslatef(0,0,-60)   
       
        glRotatef(self.y_axis,0,1,0)
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.samping1_id)
        
        for vertices in self.vertice:
			glBegin(GL_QUADS)
			for i,v in enumerate(self.faces[0]):
				glTexCoord2fv(self.texcoord[i])
				glVertex3fv(vertices[v -1])
			glEnd()
			
			glBegin(GL_QUADS)
			for i,v in enumerate(self.faces[1]):
				glTexCoord2fv(self.texcoord[i])
				glVertex3fv(vertices[v -1])
			glEnd()
			
			glBindTexture(GL_TEXTURE_2D,self.samping2_id)
			glBegin(GL_QUADS)
			for i,v in enumerate(self.faces[2]):
				glTexCoord2fv(self.texcoord[i])
				glVertex3fv(vertices[v -1])
			glEnd()
			
			glBindTexture(GL_TEXTURE_2D,self.belakang_id)
			glBegin(GL_QUADS)
			for i,v in enumerate(self.faces[3]):
				glTexCoord2fv(self.texcoord[i])
				glVertex3fv(vertices[v -1])
			glEnd()
			
			glBindTexture(GL_TEXTURE_2D,self.samping1_id)
			glBegin(GL_QUADS)
			for i,v in enumerate(self.faces[4]):
				glTexCoord2fv(self.texcoord[i])
				glVertex3fv(vertices[v -1])
			glEnd()
			
			glBindTexture(GL_TEXTURE_2D,self.depan_id)
			glBegin(GL_QUADS)
			for i,v in enumerate(self.faces[5]):
				glTexCoord2fv(self.texcoord[i])
				glVertex3fv(vertices[v -1])
			glEnd()
        
        glDisable(GL_TEXTURE_2D)
        self.y_axis = self.y_axis - 1
    
def main():
    pygame.init()
    pygame.display.set_mode((WIDTH,HEIGHT),pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.display.set_caption("Xiaomi")
    clock = pygame.time.Clock()
    done = False
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(45,1.0 * WIDTH/HEIGHT ,0.1,200.0)
    
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

