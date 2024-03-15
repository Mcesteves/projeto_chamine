#version 410
layout (vertices = 2) out;

in vec3 pgeom[];

patch out mat4 transformation[];
patch out float radius;

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
	
	mat4 translation_matrix;
	mat4 rotation_matrix;
	mat4 scale_matrix;
	vec3 d = pgeom[1] - pgeom[0];

	setTranslationMatrix(pgeom[0], translation_matrix);
	setScaleMatrix(vec3(0.2f, length(d), 0.2f), scale_matrix);
	setRotationMatrix(d, rotation_matrix);

	transformation[0] = translation_matrix;
	transformation[1] = scale_matrix;
	transformation[2] = rotation_matrix;

	radius = 1.0f;
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