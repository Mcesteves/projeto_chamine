#version 410

layout (quads) in;

#define pi 3.14159265

const vec4 leye = vec4(2.0f, 3.0f, 5.0f, 1.0f);
uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;
uniform float thickness;

patch in data{
	mat4 transformation;
	float out_radius;
	float height;
	float angle;
	float d1;
	float d2;
	int no_curve;
	float start_angle;
} mesh_data;

patch in vec4 color[3];

out data {
	vec3 neye;
	vec3 veye;
	vec3 light;
	vec4 color;
} v;

void main(){

	float theta = 2*pi*gl_TessCoord.x + mesh_data.start_angle;
	
	vec4 vpos;
	vec4 vnorm;
	float phi;
	float R = mesh_data.out_radius;
	float cylinder_percent = 0.1f;
	float k = mesh_data.height - mesh_data.d2 - mesh_data.d1;

	if(mesh_data.no_curve == 0){
		k = k/cylinder_percent;
	}

	if (gl_TessCoord.y > cylinder_percent && mesh_data.no_curve == 0){
		phi = (1/(1-cylinder_percent))*mesh_data.angle*(gl_TessCoord.y - cylinder_percent);
		vpos.x = -(-R + (R + thickness*cos(theta))*cos(phi));
		vpos.y = mesh_data.height - mesh_data.d2 + (R + thickness*cos(theta))*sin(phi);
		vpos.z = thickness * sin(theta);
		vpos.w = 1.0f;

		vnorm.x = -cos(theta)*cos(phi);
		vnorm.y = sin(phi)*cos(theta);
		vnorm.z = sin(theta);
	}
	else {
		vpos.x = -thickness * cos(theta);
		vpos.y = gl_TessCoord.y*k + mesh_data.d1;
		vpos.z = thickness * sin(theta);
		vpos.w = 1.0f;

		vnorm = vpos;
		vnorm.y = 0;
	}
	
	mat4 m = mesh_data.transformation;
	vpos = m*vpos;
	m = transpose(inverse(m));
	vnorm = m*vnorm;
	v.veye = vec3(mv*vpos);

	if (leye.w == 0)
		v.light = normalize(vec3(leye));
	else
		v.light = normalize(vec3(leye) - v.veye);
	v.neye = normalize(vec3(mn*vnorm));

	v.color = color[1];

	gl_Position = mvp * vpos;
}