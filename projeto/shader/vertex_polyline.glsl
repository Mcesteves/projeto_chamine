#version 410
layout (location = 0) in vec3 geom;
uniform vec4 light;

uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;

void main()
{
	gl_Position = mvp * vec4(geom, 1.0f);
}