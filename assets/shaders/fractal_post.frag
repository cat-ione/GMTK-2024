#version 330 core

uniform sampler2D u_imageTexture;
uniform vec2 u_texSize;
uniform float u_time;
uniform float u_zoomFactor;

in vec2 fragmentTexCoord;

out vec4 color;

vec2 pixel = 1.0 / u_texSize;
const int blurSize = 4;

void main() {
    color = vec4(0.0, 0.0, 0.0, 1.0);

    for (float i = -blurSize; i <= blurSize; i++) {
        for (float j = -blurSize; j <= blurSize; j++) {
            vec2 texCoord = fragmentTexCoord + vec2(i * pixel.x, j * pixel.y);
            color += texture(u_imageTexture, texCoord);
        }
    }

    color /= float((2 * blurSize + 1) * (2 * blurSize + 1));

    if (color.x < 0.21) {
        color = vec4(0.0, 0.0, 0.0, 1.0);
    } else if (color.x < 0.24) {
        color = vec4(0.06, 0.06, 0.06, 1.0);
    } else {
        color = vec4(0.03, 0.03, 0.03, 1.0);
    }
}
