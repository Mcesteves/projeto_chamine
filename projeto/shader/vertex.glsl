#version 410
layout (location = 0) in vec4 geom;
layout (location = 1) in vec4 color;

out vec4 pgeom;
out vec4 pcolor;

void main()
{
	pgeom = geom;
	pcolor = color;
}