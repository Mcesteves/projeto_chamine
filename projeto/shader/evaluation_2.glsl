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
patch in float alfa;

out data {
	vec3 neye;
	vec3 veye;
	vec3 light;
} v;

void main(){

	float theta = 2*pi*gl_TessCoord.x;
	
	vec4 vpos;
	vec4 vnorm;
	float phi;
	float R = 0.8f;

	if (gl_TessCoord.y > 0.75f){
		phi = 4*alfa*(gl_TessCoord.y - 0.75);
		vpos.x = -R + (R + radius*sin(theta))*cos(phi);
		vpos.y = 0.75*height + (R + radius*sin(theta))*sin(phi);;
		vpos.z = radius * cos(theta);
		vpos.w = 1.0f;
	}
	else{
		vpos.x = radius * sin(theta);
		vpos.y = gl_TessCoord.y * height;
		vpos.z = radius * cos(theta);
		vpos.w = 1.0f;
	}
	
	if (gl_TessCoord.y <= 0.75f){
		vnorm = vpos;
		vnorm.y = 0;
	}
	else{
		vnorm.x = sin(theta)*cos(phi);
		vnorm.y = sin(phi)*sin(theta);
		vnorm.z = cos(theta);
	}
	
	mat4 m = transformation;
	//mat4 m = mat4(1.0f);
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