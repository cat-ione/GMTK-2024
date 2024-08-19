#version 330 core

uniform sampler2D u_imageTexture;
uniform vec2 u_texSize;

in vec2 fragmentTexCoord;

out vec4 color;

vec2 pixel = 1.0 / u_texSize;

void main() {
    vec4 sum = vec4(0.0);
    for (int i = -1; i <= 1; i++) {
        for (int j = -1; j <= 1; j++) {
            vec2 offset = vec2(i, j) * pixel;
            sum += texture2D(u_imageTexture, fragmentTexCoord + offset);
        }
    }
    color = sum / 9.0;
}
