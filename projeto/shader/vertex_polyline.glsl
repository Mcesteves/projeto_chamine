#version 410
layout (location = 0) in vec3 geom;

uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;

out vec3 pgeom;

void main()
{
	pgeom = geom;
	gl_Position = mvp * vec4(pgeom, 1.0f);
}