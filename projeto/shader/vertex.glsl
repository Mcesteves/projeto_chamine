#version 410
layout (location = 0) in vec3 geom;

out vec3 pgeom;

void main()
{
	pgeom = geom;
}