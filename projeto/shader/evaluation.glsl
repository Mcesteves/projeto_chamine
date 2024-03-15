#version 410

layout (quads) in;

#define pi 3.14159265

const vec4 leye = vec4(2.0f, 3.0f, 5.0f, 1.0f);
uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;

patch in mat4 transformation[];
patch in float radius;

out data {
	vec3 neye;
	vec3 veye;
	vec3 light;
} v;

void main(){

	float theta = 2*pi*gl_TessCoord.x;
	vec4 vpos;

	vpos.x = radius * sin(theta);
	vpos.y = gl_TessCoord.y;
	vpos.z = radius * cos(theta);
	vpos.w = 1.0f;

	vpos = transformation[0]*transformation[2]*transformation[1]*vpos;
	v.veye = vec3(mv*vpos);

	if (leye.w == 0)
		v.light = normalize(vec3(leye));
	else
		v.light = normalize(vec3(leye) - v.veye);
	v.neye = normalize(vec3(mn*vpos));

	gl_Position = mvp * vpos;
}