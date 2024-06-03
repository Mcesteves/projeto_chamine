#version 410
layout (vertices = 5) out;

in vec4 pgeom[];
in vec4 pcolor[];

#define pi 3.14159265
uniform int subdivision;
uniform float curve_percent;

patch out data{
	mat4 transformation;
	float out_radius;
	float height;
	float angle;
	float d1;
	float d2;
	int no_curve;
	float start_angle;
	float next_height;
	float next_d2;
	float next_radius;
	float next_angle;
	float pre_angle;
} mesh_data;

patch out vec4 color[3];

mat4 createOrthogonalBasis(vec3 d, vec3 y){
	vec3 z = cross(normalize(d), y);
	vec3 x = cross(normalize(y), normalize(z));

	if(z == vec3(0.0f)){
		z = cross(normalize(d), vec3(-d.y, d.x, 0.0f));
		if(z == vec3(0.0f))
			z = cross(normalize(d), vec3(-d.z, 0.0f, d.x));
			if(z == vec3(0.0f))
				z = cross(normalize(d), vec3(0.0f, -d.z, d.y));
	}
	x = cross(normalize(y), normalize(z));
	return mat4(vec4(normalize(x),0.0f),
				vec4(normalize(y), 0.0f),
				vec4(normalize(z), 0.0f), 
				vec4(0.0, 0.0, 0.0, 1.0));
}

void setTranslationMatrix(vec3 t, out mat4 t_matrix){
	t_matrix = mat4(
		vec4(1.0, 0.0, 0.0, 0.0),
		vec4(0.0, 1.0, 0.0, 0.0),
		vec4(0.0, 0.0, 1.0, 0.0),
		vec4(t.x, t.y, t.z, 1.0)
	);
}

float CalculateTorusAngle(vec3 c1, vec3 c2){
	vec3 v1 = normalize(c1);
	vec3 v2 = normalize(c2);
	float dot_p = dot(v1, v2);

	if(dot_p < -0.999999f && dot_p > -1.0f)
		return pi;

	if(dot_p < 1.0f && dot_p > 0.999999f)
		return 0.0f;

	return acos(dot(v1, v2));
}

void main(){
	mat4 translation_matrix;
	mesh_data.no_curve = 0;

	vec3 v1 = vec3(pgeom[1]) - vec3(pgeom[0]);
	vec3 v2 = vec3(pgeom[2]) - vec3(pgeom[1]);
	vec3 v3 = vec3(pgeom[3]) - vec3(pgeom[2]);
	vec3 v4 = vec3(pgeom[4]) - vec3(pgeom[3]);

	if( v3 == vec3(0.0f)){
		v3 = (normalize(v2));
	}
	if( v4 == vec3(0.0f)){
		v4 = normalize(v3);
	}

	mat4 local_to_global = createOrthogonalBasis(v3, v2);

	float beta = CalculateTorusAngle(v1,v2);
	float theta = CalculateTorusAngle(v2,v3);
	float alpha = CalculateTorusAngle(v3,v4);

	float d1 = min(curve_percent*length(v1), curve_percent*length(v2));
	float d2 = min(curve_percent*length(v2), curve_percent*length(v3));
	float next_d2 = min(curve_percent*length(v3), curve_percent*length(v4));
	
	if(beta == 0.0f){
		d1 = 0.0f;
	}
	if(theta == 0.0f){
		d2 = 0.0f;
		mesh_data.no_curve = 1;
	}
	if(alpha == 0.0f){
		next_d2 = 0.0f;
	}
	
	float r2 = d2*(1/tan(theta/2));
	float next_radius = next_d2*(1/tan(alpha/2));
	setTranslationMatrix(vec3(pgeom[1]), translation_matrix);

	mesh_data.start_angle = pgeom[2].w;
	mesh_data.transformation = translation_matrix*local_to_global;
	mesh_data.angle = theta;
	mesh_data.out_radius = r2;
	mesh_data.height = length(v2);
	mesh_data.d1 = d1;
	mesh_data.d2 = d2;
	mesh_data.next_height = length(v3);
	mesh_data.next_d2 = next_d2;
	mesh_data.next_radius = next_radius;
	mesh_data.next_angle = alpha;
	mesh_data.pre_angle = beta;

	vec4 color_vec[3] = vec4[3](pcolor[1], pcolor[2], pcolor[3]);
	color = color_vec;
	
	if (gl_InvocationID == 0)
	{
		gl_TessLevelOuter[0] = subdivision;
		gl_TessLevelOuter[1] = subdivision;
		gl_TessLevelOuter[2] = subdivision;
		gl_TessLevelOuter[3] = subdivision;
		gl_TessLevelInner[0] = subdivision;
		gl_TessLevelInner[1] = subdivision;
	}

}