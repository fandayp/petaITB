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
from OpenGL import GL as gl
from OpenGL.arrays import vbo
from OpenGL.GL.shaders import compileProgram, compileShader
from texture import Texture

DLIGHT_FUNC = """
float dLight(
    in vec3 light_pos, // normalised light position
    in vec3 frag_normal // normalised geometry normal
) {
    // returns vec2( ambientMult, diffuseMult )
    float n_dot_pos = max( 0.0, dot(
        frag_normal, light_pos
    ));
    return n_dot_pos;
}
"""

VERTEX_SHADER = DLIGHT_FUNC + '''
uniform vec4 Global_ambient;
uniform vec4 Light_ambient;
uniform vec4 Light_diffuse;
uniform vec3 Light_location;
uniform vec4 Material_ambient;
uniform vec4 Material_diffuse;

attribute vec3 Vertex_position;
attribute vec2 Vertex_texCoord;
attribute vec3 Vertex_normal;

varying vec4 baseColor;
varying vec2 texCoord0;

void main() {

    gl_Position = gl_ModelViewProjectionMatrix * vec4(
        Vertex_position, 1.0
    );

    vec3 EC_Light_location = gl_NormalMatrix * Light_location;
    float diffuse_weight = dLight(
        normalize(EC_Light_location),
        normalize(gl_NormalMatrix * Vertex_normal)
    );

    texCoord0 = Vertex_texCoord;

    baseColor = clamp(
    (
        // global component
        (Global_ambient * Material_ambient)

        // material's interaction with light's contribution
        // to the ambient lighting...
        + (Light_ambient * Material_ambient)

        // material's interaction with the direct light from
        // the light.
        + (Light_diffuse * Material_diffuse * diffuse_weight)
    ), 0.0, 1.0);
}
'''

FRAGMENT_SHADER = '''
varying vec4 baseColor;
varying vec2 texCoord0;

uniform sampler2D diffuse;

void main() {
    gl_FragColor = texture2D(diffuse, texCoord0) * baseColor;
}
'''

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
                compileShader( VERTEX_SHADER, gl.GL_VERTEX_SHADER ),
                compileShader( FRAGMENT_SHADER, gl.GL_FRAGMENT_SHADER )
            )
        except RuntimeError, err:
            sys.stderr.write( err.args[0] )
            sys.exit( 1 )

        # vertex buffer object
        self.vertices = vbo.VBO(
            array( VERTEX_DATA, 'f' )
        )

        self.indices = vbo.VBO(
            array(VERTEX_INDICES, 'uint32'),
            target='GL_ELEMENT_ARRAY_BUFFER'
        )

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
            location = gl.glGetUniformLocation( self.shader, uniform )
            if location in ( None, -1 ):
                print 'Warning, no uniform: %s'%( uniform )
            setattr( self, uniform+ '_loc', location )

        for attribute in (
            'Vertex_position',
            'Vertex_texCoord',
            'Vertex_normal',
        ):
            location = gl.glGetAttribLocation( self.shader, attribute )
            if location in ( None, -1 ):
                print 'Warning, no attribute: %s'%( attribute )
            setattr( self, attribute + '_loc', location )

    def Render( self, mode ):
        '''
        render the scene geometry
        '''
        gl.glUseProgram( self.shader )
        try:
            self.vertices.bind()
            self.indices.bind()
            self.tex[0].Bind(0)

            try:
                gl.glUniform4f( self.Global_ambient_loc, .9,.05,.05,.1 )
                gl.glUniform4f( self.Light_ambient_loc, .2,.2,.2, 1.0 )
                gl.glUniform4f( self.Light_diffuse_loc, 1,1,1,1 )

                gl.glUniform3f( self.Light_location_loc, 2,2,10 )
                gl.glUniform4f( self.Material_ambient_loc, .2,.2,.2, 1.0 )
                gl.glUniform4f( self.Material_diffuse_loc, 1,1,1, 1 )

                stride = 8*4 # x y z x_tex y_tex r g b * sizeof(float)
                gl.glEnableVertexAttribArray( self.Vertex_position_loc ) # 0
                gl.glEnableVertexAttribArray( self.Vertex_texCoord_loc ) # 1
                gl.glEnableVertexAttribArray( self.Vertex_normal_loc ) # 2

                # bind the vertex attribute location
                gl.glVertexAttribPointer(
                    self.Vertex_position_loc,
                    3, gl.GL_FLOAT,False, stride, self.vertices
                )

                gl.glVertexAttribPointer(
                	self.Vertex_texCoord_loc,
                	2, gl.GL_FLOAT,False, stride, self.vertices+12
                )

                gl.glVertexAttribPointer( 
                    self.Vertex_normal_loc,
                    3, gl.GL_FLOAT,False, stride, self.vertices+20
                )

                # musti diubah jadi indices biar lebih gampang
                gl.glDrawElements(gl.GL_TRIANGLES, 18, gl.GL_UNSIGNED_INT, None)

                #gl.glDrawArrays(gl.GL_TRIANGLES, 0, 18)
            finally:
                self.vertices.unbind()
                self.indices.unbind()

                gl.glDisableVertexAttribArray( self.Vertex_position_loc )
                gl.glDisableVertexAttribArray( self.Vertex_texCoord_loc )
                gl.glDisableVertexAttribArray( self.Vertex_normal_loc )

        finally:
            gl.glUseProgram(0)


if __name__ == "__main__":
    TestContext.ContextMainLoop()
