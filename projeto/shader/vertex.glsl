#version 410
layout (location = 0) in vec4 geom;

out vec4 pgeom;

void main()
{
	pgeom = geom;
}