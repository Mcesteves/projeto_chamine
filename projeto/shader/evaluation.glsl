#version 410

layout (quads) in;

#define pi 3.14159265

const vec4 leye = vec4(2.0f, 3.0f, 5.0f, 1.0f);
uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;

patch in vec3 pos[2];
patch in float radius;

out data {
	vec3 neye;
	vec3 veye;
	vec3 light;
} v;

void setTranslationMatrix(vec3 t, out mat4 t_matrix){
	t_matrix = mat4(
		vec4(1.0, 0.0, 0.0, 0.0),
		vec4(0.0, 1.0, 0.0, 0.0),
		vec4(0.0, 0.0, 1.0, 0.0),
		vec4(t.x, t.y, t.z, 1.0)
	);
}

void setScaleMatrix(vec3 s, out mat4 s_matrix){
	s_matrix = mat4(
		vec4(s.x, 0.0, 0.0, 0.0),
		vec4(0.0, s.y, 0.0, 0.0),
		vec4(0.0, 0.0, s.z, 0.0),
		vec4(0.0, 0.0, 0.0, 1.0)
	);
}

void setRotationMatrix(vec3 d, out mat4 r_matrix){
	d = normalize(d);
	vec3 j = vec3(0,1,0);
	vec3 r = cross(d, j);
	
	if(r == vec3(0,0,0))
	{
		r_matrix = mat4(1.0);
		return;
	}
	float theta = acos(dot(j, d));

	float c = cos(theta);
	float s = sin(theta);
	float t = 1 - cos(theta);
	vec3 r_unit = normalize(r);

	r_matrix = mat4(
		vec4(t * pow(r_unit.x, 2) + c, t * r_unit.x * r_unit.y - s * r_unit.z, t * r_unit.x * r_unit.z + s * r_unit.y, 0.0),
		vec4(t * r_unit.x * r_unit.y + s * r_unit.z, t * pow(r_unit.y, 2) + c, t * r_unit.y * r_unit.z - s * r_unit.x, 0.0),
		vec4(t * r_unit.x * r_unit.z - s * r_unit.y, t * r_unit.y * r_unit.z + s * r_unit.x, t * pow(r_unit.z, 2) + c, 0.0),
		vec4(0.0, 0.0, 0.0, 1.0)
	);
}

void main(){

	float theta = 2*pi*gl_TessCoord.x;
	vec4 vpos;
	mat4 rotation_matrix;
	mat4 translation_matrix;
	mat4 scale_matrix;
	vec3 d = pos[1] - pos[0];

	setTranslationMatrix(pos[0], translation_matrix);
	setRotationMatrix(d, rotation_matrix);
	setScaleMatrix(vec3(0.2f, length(d), 0.2f), scale_matrix);

	vpos.x = radius * sin(theta);
	vpos.y = gl_TessCoord.y;
	vpos.z = radius * cos(theta);
	vpos.w = 1.0f;

	vpos = translation_matrix*rotation_matrix*scale_matrix*vpos;
	v.veye = vec3(mv*vpos);

	if (leye.w == 0)
		v.light = normalize(vec3(leye));
	else
		v.light = normalize(vec3(leye) - v.veye);
	v.neye = normalize(vec3(mn*vpos));

	gl_Position = mvp * vpos;
}