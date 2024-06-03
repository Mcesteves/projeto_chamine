#version 410

layout (quads) in;

#define pi 3.14159265

const vec4 leye = vec4(2.0f, 3.0f, 5.0f, 1.0f);
uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;
uniform float thickness;

patch in data{
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

patch in vec4 color[3];

out data {
	vec3 neye;
	vec3 veye;
	vec3 light;
	vec4 color;
} v;

void main(){
	int is_curve = 0;
	int change_color = 0;
	float theta = 2*pi*gl_TessCoord.x + mesh_data.start_angle;
	vec4 vpos;
	vec4 vnorm;
	float phi;
	float cylinder_percent = 0.1f;
	float k = mesh_data.height - mesh_data.d2 - mesh_data.d1;

	if(mesh_data.no_curve == 0){
		k = k/cylinder_percent;
	}
	
	if (gl_TessCoord.y > cylinder_percent && mesh_data.no_curve == 0){
		is_curve = 1;
		phi = (1/(1-cylinder_percent))*mesh_data.angle*(gl_TessCoord.y - cylinder_percent);
		if(phi >= mesh_data.angle/2.0f){
			change_color = 1;
		}
		vpos.x = -(-mesh_data.out_radius + (mesh_data.out_radius + thickness*cos(theta))*cos(phi));
		vpos.y = mesh_data.height - mesh_data.d2 + (mesh_data.out_radius + thickness*cos(theta))*sin(phi);
		vpos.z = thickness * sin(theta);
		vpos.w = 1.0f;

		vnorm.x = -cos(theta)*cos(phi);
		vnorm.y = sin(phi)*cos(theta);
		vnorm.z = sin(theta);
	}
	else {
		vpos.x = -thickness * cos(theta);
		vpos.y = gl_TessCoord.y*k + mesh_data.d1;
		vpos.z = thickness * sin(theta);
		vpos.w = 1.0f;
		//if(vpos.y > mesh_data.height - mesh_data.d2)
			//change_color = 1;

		vnorm = vpos;
		vnorm.y = 0;
	}
	
	mat4 m = mesh_data.transformation;
	vpos = m*vpos;
	m = transpose(inverse(m));
	vnorm = m*vnorm;
	v.veye = vec3(mv*vpos);

	if (leye.w == 0)
		v.light = normalize(vec3(leye));
	else
		v.light = normalize(vec3(leye) - v.veye);
	v.neye = normalize(vec3(mn*vnorm));

	float t, h1;
	float c = (mesh_data.angle)*mesh_data.out_radius;
	vec4 color_1, color_2;
	if(change_color == 0){
		if(mesh_data.no_curve == 1)
			if(mesh_data.d1 == 0.0f){
				h1 = mesh_data.height - mesh_data.d2/2.0f;
				t = (gl_TessCoord.y * h1 + mesh_data.d1)/h1;
			}
			else{
				h1 = mesh_data.height - mesh_data.d2/2.0f - mesh_data.d1 + mesh_data.pre_angle*mesh_data.d1*(1/tan(mesh_data.pre_angle/2)/2.0f);
				t = (gl_TessCoord.y * h1 + mesh_data.pre_angle*mesh_data.d1*(1/tan(mesh_data.pre_angle/2)/2.0f))/h1;
			}
		else{
			if(mesh_data.d1 == 0.0f){
				h1 = mesh_data.height - mesh_data.d2 + c/2.0f;
				t = (gl_TessCoord.y * h1 + mesh_data.d1)/h1;
			}	
			else{
				h1 = mesh_data.height - mesh_data.d2 + c/2.0f - mesh_data.d1 + mesh_data.pre_angle*mesh_data.d1*(1/tan(mesh_data.pre_angle/2)/2.0f);
				t = (gl_TessCoord.y * h1 + mesh_data.pre_angle*mesh_data.d1*(1/tan(mesh_data.pre_angle/2)/2.0f))/h1;
			}
		}
		if(is_curve == 1){
			t = (gl_TessCoord.y*(1/(1-cylinder_percent))*c/2.0f + h1 - c/2.0f)/h1;
		}
		color_1 = color[0];
		color_2 = color[1];
	}
	else{
		float h2;
		if(mesh_data.no_curve == 1){
			h2 = mesh_data.next_height - mesh_data.next_d2/2.0f;
			t = (gl_TessCoord.y*(1/(1-cylinder_percent))*mesh_data.d2/2.0f)/h2;
		}
		else{
			if(mesh_data.next_angle == 0.0f){
				h2 = mesh_data.next_height - mesh_data.next_d2/2.0f;
				t = (gl_TessCoord.y*(1/(1-cylinder_percent))*mesh_data.d2/2.0f)/h2;
			}
			else{
				float c2 = mesh_data.next_angle*mesh_data.next_radius;
				h2 = mesh_data.next_height - mesh_data.next_d2 + c2/2.0f;
				t = (gl_TessCoord.y*(1/(1-cylinder_percent))*c/2.0f)/h2;
			}			
		}
			
		color_1 = color[1];
		color_2 = color[2];
	}
	v.color.r = color_1.r + (color_2.r - color_1.r) * t;
	v.color.g = color_1.g + (color_2.g - color_1.g) * t;
	v.color.b = color_1.b + (color_2.b - color_1.b) * t;
	v.color.a = color_1.a + (color_2.a - color_1.a) * t;

	gl_Position = mvp * vpos;
}