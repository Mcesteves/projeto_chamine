#version 410
layout (vertices = 4) out;

in vec3 pgeom[];

patch out data{
	mat4 transformation;
	float out_radius;
	float in_radius;
	float height;
	float angle;
	float d1;
} mesh_data;

void setTranslationMatrix(vec3 t, out mat4 t_matrix){
	t_matrix = mat4(
		vec4(1.0, 0.0, 0.0, 0.0),
		vec4(0.0, 1.0, 0.0, 0.0),
		vec4(0.0, 0.0, 1.0, 0.0),
		vec4(t.x, t.y, t.z, 1.0)
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

float CalculateTorusAngle(vec3 c1, vec3 c2){

	c1 = normalize(c1);
	c2 = normalize(c2);

	float angle = acos(dot(c1, c2));
	return angle;
}

void main(){
	
	mat4 translation_matrix;
	mat4 rotation_matrix;

	vec3 v1 = pgeom[1] - pgeom[0];
	vec3 v2 = pgeom[2] - pgeom[1];
	vec3 v3 = pgeom[3] - pgeom[2];

	float beta = CalculateTorusAngle(v1,v2);
	float theta = CalculateTorusAngle(v2,v3);

	float d1 = 0.25*length(v1);
	float d2 = 0.25*length(v2);
	
	float r1 = d1*(1/tan(beta/2));
	float r2 = d2*(1/tan(theta/2));
	
	setTranslationMatrix(pgeom[1], translation_matrix);
	setRotationMatrix(v2, rotation_matrix);

	mesh_data.transformation = translation_matrix*rotation_matrix;
	mesh_data.angle = theta;
	mesh_data.out_radius = r2;
	mesh_data.in_radius = 0.2f;
	mesh_data.height = length(v2);
	mesh_data.d1 = d1;
	
	if (gl_InvocationID == 0)
	{
		gl_TessLevelOuter[0] = 64;
		gl_TessLevelOuter[1] = 64;
		gl_TessLevelOuter[2] = 64;
		gl_TessLevelOuter[3] = 64;
		gl_TessLevelInner[0] = 64;
		gl_TessLevelInner[1] = 64;
	}

}