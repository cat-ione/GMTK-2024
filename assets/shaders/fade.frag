#version 330 core

uniform sampler2D u_imageTexture;
uniform vec2 u_texSize;
uniform float u_alpha;

in vec2 fragmentTexCoord;

out vec4 color;

vec2 pixel = 1.0 / u_texSize;

void main() {
    color = texture2D(u_imageTexture, fragmentTexCoord);
    color.a *= u_alpha;
}
