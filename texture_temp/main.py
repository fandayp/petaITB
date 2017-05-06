'''
This tutorial builds on earlier tutorials by adding:
    * 	ambient lighting
    * 	diffuse lighting
    * 	directional lights (e.g. the Sun)
    * 	normals, the normal matrix
'''
import sys

from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()
from OpenGLContext.arrays import array
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GL.shaders import compileProgram, compileShader

# import from other files
from texture import Texture
from shaders.vertexShader import *
from shaders.fragmentShader import *

VERTEX_DATA = [
#      x,  y,  z, x_tex, y_tex, r,  g,  b
    [ -1, 0, 0, 0, 0, -1, 0, 1],
    [  0, 0, 1, 0.1, 0.1, -1, 0, 2],
    [  0, 1, 1, 0, 0.1, -1, 0, 2],
    [ -1, 0, 0, 0.2, 0.2, -1, 0, 1],
    [  0, 1, 1, 0.2, 0.3, -1, 0, 2],
    [ -1, 1, 0, 0.3, 0.3, -1, 0, 1],
    [  0, 0, 1, 0.4, 0.4, -1, 0, 2],
    [  1, 0, 1, 0.1, 0.1, 1, 0, 2],
    [  1, 1, 1, 0.4, 0.1, 1, 0, 2],
    [  0, 0, 1, 0.5, 0.5, -1, 0, 2],
    [  1, 1, 1, 0.7, 0.5, 1, 0, 2],
    [  0, 1, 1, 0.7, 0.7, -1, 0, 2],
    [  1, 0, 1, 0.8, 0.8, 1, 0, 2],
    [  2, 0, 0, 0.8, 1.0, 1, 0, 1],
    [  2, 1, 0, 1.0, 1.0, 1, 0, 1],
    [  1, 0, 1, 0.0, 0.0, 1, 0, 2],
    [  2, 1, 0, 1.0, 0.0, 1, 0, 1],
    [  1, 1, 1, 1.0, 1.0, 1, 0, 2],
]

VERTEX_INDICES = [
	0, 1, 2,
	3, 4, 5,
	6, 7, 8,
	9, 10, 11,
	12, 13, 14,
	15, 16, 17,
]

class TestContext( BaseContext ):
    '''
    creates a simple vertex shader
    '''
    def OnInit( self ):
        try:
            self.shader = compileProgram(
                compileShader( VERTEX_SHADER, GL_VERTEX_SHADER ),
                compileShader( FRAGMENT_SHADER, GL_FRAGMENT_SHADER )
            )
        except RuntimeError, err:
            sys.stderr.write( err.args[0] )
            sys.exit( 1 )

        # vertex buffer object
        self.vertices = vbo.VBO(array(VERTEX_DATA, 'f'))

        self.indices = vbo.VBO(array(VERTEX_INDICES, 'uint32'),target='GL_ELEMENT_ARRAY_BUFFER')

        # import texture
        self.tex = [
            Texture('res/depan.jpg'),
            Texture('res/belakang.jpg'),
            Texture('res/samping.jpg'),
            Texture('res/samping2.jpg'),
        ]

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
                print 'Warning, no uniform: %s'%( uniform )
            setattr( self, uniform+ '_loc', location )

        for attribute in (
            'Vertex_position',
            'Vertex_texCoord',
            'Vertex_normal',
        ):
            location = glGetAttribLocation( self.shader, attribute )
            if location in ( None, -1 ):
                print 'Warning, no attribute: %s'%( attribute )
            setattr( self, attribute + '_loc', location )

    def Render( self, mode ):
        '''
        render the scene geometry
        '''
        glUseProgram( self.shader )
        try:
            self.vertices.bind()
            self.indices.bind()

            try:

                # BEGIN OF LIGHTING INITIALIZATION
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

                # starting of binding different textures with draw Elements

                self.tex[0].Bind(0)
                # musti diubah jadi indices biar lebih gampang
                glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, None)

                #glDrawArrays(GL_TRIANGLES, 0, 18)
            finally:
                self.vertices.unbind()
                self.indices.unbind()

                glDisableVertexAttribArray( self.Vertex_position_loc )
                glDisableVertexAttribArray( self.Vertex_texCoord_loc )
                glDisableVertexAttribArray( self.Vertex_normal_loc )

        finally:
            glUseProgram(0)


if __name__ == "__main__":
    TestContext.ContextMainLoop()
