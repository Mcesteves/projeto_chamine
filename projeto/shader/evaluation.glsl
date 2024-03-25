#version 410

layout (quads) in;

#define pi 3.14159265

const vec4 leye = vec4(2.0f, 3.0f, 5.0f, 1.0f);
uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;

patch in mat4 transformation;
patch in float radius;
patch in float height;

out data {
	vec3 neye;
	vec3 veye;
	vec3 light;
} v;

void main(){

	float theta = 2*pi*gl_TessCoord.x;
	vec4 vpos;
	vec4 vnorm;

	vpos.x = radius * sin(theta);
	vpos.y = gl_TessCoord.y * height;
	vpos.z = radius * cos(theta);
	vpos.w = 1.0f;

	vnorm = vpos;
	vnorm.y = 0;

	mat4 m = transformation;
	vpos = m*vpos;
	m = transpose(inverse(m));
	
	vnorm = m*vnorm;
	v.veye = vec3(mv*vpos);


	if (leye.w == 0)
		v.light = normalize(vec3(leye));
	else
		v.light = normalize(vec3(leye) - v.veye);
	v.neye = normalize(vec3(mn*vnorm));

	gl_Position = mvp * vpos;
}