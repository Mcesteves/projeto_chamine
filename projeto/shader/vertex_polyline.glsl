#version 410
layout (location = 0) in vec3 geom;
layout (location = 0) in vec3 t;
uniform vec4 light;

uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;

out vec3 out_t;
out vec3 out_l;

void main()
{
	gl_Position = mvp * vec4(geom, 1.0f);
	out_t = t;
	out_l = vec3(light) - geom;
}