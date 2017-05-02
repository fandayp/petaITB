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

    texCoord0 = Vertex_texCoord;
    gl_Position = gl_ModelViewProjectionMatrix * vec4(
        Vertex_position, 1.0
    );


    // code below is for lighting, 
    // from global, material, and light ambient
    // and clamp with the baseColor

    vec3 EC_Light_location = gl_NormalMatrix * Light_location;
    float diffuse_weight = dLight(
        normalize(EC_Light_location),
        normalize(gl_NormalMatrix * Vertex_normal)
    );

   

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