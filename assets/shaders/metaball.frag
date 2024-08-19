#version 330 core

uniform int u_metaballCount;
uniform vec3[400] u_metaballs;
uniform int u_antiballCount;
uniform vec3[100] u_antiballs;
uniform sampler2D u_imageTexture;
uniform vec2 u_texSize;

in vec2 fragmentTexCoord;

out vec4 color;

vec2 pixel = 1.0 / u_texSize;

void main() {
    vec2 coord = vec2(fragmentTexCoord / pixel);
    coord.y = u_texSize.y - coord.y;

    float sum = 0.0;
    for (int i = 0; i < u_metaballCount; i++) {
        vec2 metaball = u_metaballs[i].xy;
        sum += pow(u_metaballs[i].z, 2) / (pow(coord.x - metaball.x, 2) + pow(coord.y - metaball.y, 2));
    }

    for (int i = 0; i < u_antiballCount; i++) {
        vec2 antiball = u_antiballs[i].xy;
        sum -= pow(u_antiballs[i].z, 2) / (pow(coord.x - antiball.x, 2) + pow(coord.y - antiball.y, 2));
    }

    color = vec4(0.0, 0.0, 0.0, 0.0);
    if (sum > 1.0) {
        color = vec4(0.0, 0.0, 0.0, 1.0);
    } else if (sum > 0.5) {
        float c = (sum - 0.5) * 0.12;
        color = vec4(1.0, 1.0, 1.0, c);
    }
}
