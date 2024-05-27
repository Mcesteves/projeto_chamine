#version 410
layout (vertices = 4) out;

in vec3 pgeom[];

#define pi 3.14159265
uniform samplerBuffer transform_buffer;
uniform samplerBuffer angle_buffer;

patch out data{
	mat4 transformation;
	float out_radius;
	float in_radius;
	float height;
	float angle;
	float d1;
	float d2;
	int no_curve;
	float start_angle;
} mesh_data;

float CalculateTorusAngle(vec3 c1, vec3 c2){

	c1 = normalize(c1);
	c2 = normalize(c2);

	float angle = acos(dot(c1, c2));
	return angle;
}

void main(){
	
	mesh_data.no_curve = 0;

	vec3 v1 = pgeom[1] - pgeom[0];
	vec3 v2 = pgeom[2] - pgeom[1];
	vec3 v3 = pgeom[3] - pgeom[2];

	if( v3 == vec3(0.0f)){
		v3 = (normalize(v2));
	}

	float beta = CalculateTorusAngle(v1,v2);
	float theta = CalculateTorusAngle(v2,v3);

	float d1 = min(0.15*length(v1), 0.15*length(v2));
	float d2 = min(0.15*length(v2), 0.15*length(v3));
	
	if(beta == 0.0f){
		d1 = 0.0f;
	}
	if(theta == 0.0f){
		d2 = 0.0f;
		mesh_data.no_curve = 1;
	}
	
	//float r1 = d1*(1/tan(beta/2));
	float r2 = d2*(1/tan(theta/2));

	vec4 line1 = texelFetch(transform_buffer, gl_PrimitiveID*3);
	vec4 line2 = texelFetch(transform_buffer, gl_PrimitiveID*3 + 1);
	vec4 line3 = texelFetch(transform_buffer, gl_PrimitiveID*3 + 2);
	mat4 transform = mat4(
		vec4(line1.x, line2.x, line3.x, 0.0f),
		vec4(line1.y, line2.y, line3.y, 0.0f),
		vec4(line1.z, line2.z, line3.z, 0.0f),
		vec4(line1.w, line2.w, line3.w, 1.0f)
		);

	int i = textureSize(angle_buffer);
	float start = 0;
	while(i >= gl_PrimitiveID){
		float angle = texelFetch(angle_buffer, i).x;
		start += angle;
		i -= 1;
	}
	
	mesh_data.start_angle = start;
	mesh_data.transformation = transform;
	mesh_data.angle = theta;
	mesh_data.out_radius = r2;
	mesh_data.in_radius = 0.05f;
	mesh_data.height = length(v2);
	mesh_data.d1 = d1;
	mesh_data.d2 = d2;
	
	if (gl_InvocationID == 0)
	{
		gl_TessLevelOuter[0] = 16;
		gl_TessLevelOuter[1] = 16;
		gl_TessLevelOuter[2] = 16;
		gl_TessLevelOuter[3] = 16;
		gl_TessLevelInner[0] = 16;
		gl_TessLevelInner[1] = 16;
	}

}