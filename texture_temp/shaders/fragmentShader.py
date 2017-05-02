FRAGMENT_SHADER = '''
varying vec4 baseColor;
varying vec2 texCoord0;

uniform sampler2D diffuse;

void main() {
    gl_FragColor = texture2D(diffuse, texCoord0) * baseColor;
}
'''