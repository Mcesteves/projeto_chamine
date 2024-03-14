#version 410
layout (vertices = 2) out;

in vec3 pgeom[];

patch out vec3 pos[2];
patch out float radius;
void main(){

	pos[gl_InvocationID] = pgeom[gl_InvocationID];
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