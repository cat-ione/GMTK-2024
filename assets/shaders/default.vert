#version 330 core

uniform vec2 u_targetSize;
uniform vec2 u_vertexOffset;

in vec3 vertexPos;
in vec2 vertexTexCoord;

out vec2 fragmentTexCoord;

vec2 norm(vec2 v) {
    return v * vec2(2 / u_targetSize.x, -2 / u_targetSize.y) + vec2(-1, 1);
}

void main() {
    gl_Position = vec4(norm(vertexPos.xy + u_vertexOffset), 0.0, 1.0);
    fragmentTexCoord = vertexTexCoord;
}
