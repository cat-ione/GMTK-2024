#version 330 core

uniform sampler2D u_imageTexture;
uniform vec2 u_texSize;
uniform float u_time;
uniform float u_zoomFactor;

in vec2 fragmentTexCoord;

out vec4 color;

vec2 pixel = 1.0 / u_texSize;

void main() {
    color = vec4(0.0, 0.0, 0.0, 1.0);
    float n = 8.0;
    for (int i = 0; i < n; i++) {
        float progress = mod(u_time * u_zoomFactor + i, n);
        float scale = exp2(progress);
        vec2 centeredCoord = (fragmentTexCoord - 0.5) * scale + 0.5;
        vec4 texColor = texture(u_imageTexture, fract(centeredCoord));
        if (texColor.x < 0.5) {
            texColor = vec4(0.0, 0.0, 0.0, 1.0);
        } else {
            texColor = vec4(1.0, 1.0, 1.0, 1.0);
        }
        color += texColor * (1.0 - progress / n) / n * smoothstep(0.0, 0.15, progress / n);
    }
    color.rgb = (color.rgb - 0.5) * 1.5 + 0.5;
    color.rgb *= max(pow(length(fragmentTexCoord - vec2(0.5)) * 2.0, 3.0), 0.4) * 0.2;
}
