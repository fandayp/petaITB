from OpenGLContext.arrays import array
from OpenGL.GL import *
import pygame

class Texture(object):
	def __init__(self, fileName):

		textureSurface = pygame.image.load(fileName)
		textureData = pygame.image.tostring(textureSurface,"RGBA",1)
		width = textureSurface.get_width()
		height = textureSurface.get_height()

		self.m_texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, self.m_texture)

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)# GL_CLAMP for not repeating more pixels
		
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR) # minification fewer pixel, GL_LINEAR interpolate linearly within pixels
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # magnification
		
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

	def Bind(self, unit):
		glActiveTexture(GL_TEXTURE0 + unit);
		glBindTexture(GL_TEXTURE_2D, self.m_texture);
