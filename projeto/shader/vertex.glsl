#version 410
layout (location = 0) in vec4 geom;
layout (location = 1) in float prop;

out vec4 pgeom;
out float pprop;

void main()
{
	pgeom = geom;
	pprop = prop;
}