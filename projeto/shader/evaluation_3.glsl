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

patch in data{
	mat4 transformation;
	float out_radius;
	float in_radius;
	float height;
	float angle;
	float d1;
} mesh_data;

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
	float R = mesh_data.out_radius;

	if (gl_TessCoord.y >= 0.75f){
		phi = 4*mesh_data.angle*(gl_TessCoord.y - 0.75);
		vpos.x = -(-R + (R + mesh_data.in_radius*sin(theta))*cos(phi));
		vpos.y = 0.75*mesh_data.height + (R + mesh_data.in_radius*sin(theta))*sin(phi);
		vpos.z = mesh_data.in_radius * cos(theta);
		vpos.w = 1.0f;
	}
	else if(gl_TessCoord.y*mesh_data.height >= mesh_data.d1){
		vpos.x = -mesh_data.in_radius * sin(theta);
		vpos.y = gl_TessCoord.y * mesh_data.height;
		vpos.z = mesh_data.in_radius * cos(theta);
		vpos.w = 1.0f;
	}
	if (gl_TessCoord.y <= 0.75f){
		vnorm = vpos;
		vnorm.y = 0;
	}
	else{
		vnorm.x = -sin(theta)*cos(phi);
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