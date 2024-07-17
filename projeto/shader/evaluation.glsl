#version 410

layout (quads) in;

#define pi 3.14159265

const vec4 leye = vec4(0.0f, 0.0f, 0.0f, 1.0f);
uniform mat4 mv;
uniform mat4 mn;
uniform mat4 mvp;
uniform float thickness;
uniform float cylinder_percent;
uniform samplerBuffer color_scale;

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
	float next_angle;
	float pre_angle;
} mesh_data;

patch in float prop[3];

out data {
	vec3 neye;
	vec3 veye;
	vec3 light;
	vec4 color;
} v;


vec3 calculateNormal(float theta, float phi){
	
	float parcial_x_theta = thickness*cos(phi)*sin(theta);
	float parcial_x_phi = thickness*cos(theta)*sin(phi);

	float parcial_y_theta = -thickness*sin(phi)*sin(theta);
	float parcial_y_phi = cos(phi)*(thickness*cos(theta) + mesh_data.out_radius);

	float parcial_z_theta = thickness*cos(theta);
	float parcial_z_phi = 0;

	vec3 par_theta_coord = vec3(parcial_x_theta, parcial_y_theta, parcial_z_theta);
	vec3 par_phi_coord = vec3(parcial_x_phi, parcial_y_phi, parcial_z_phi);

	vec3 vnorm = cross(par_theta_coord, par_phi_coord);

	return vnorm;
}

void main(){
	int is_curve = 0;
	int change_color = 0;
	float theta = 2*pi*gl_TessCoord.x + mesh_data.start_angle;
	vec4 vpos;
	vec4 vnorm;
	float phi;
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

		vnorm = vec4(calculateNormal(theta, phi), 1.0f);
	}
	else {
		vpos.x = -thickness * cos(theta);
		vpos.y = gl_TessCoord.y*k + mesh_data.d1;
		vpos.z = thickness * sin(theta);
		vpos.w = 1.0f;
		if(vpos.y > mesh_data.height - mesh_data.d2)
			change_color = 1;

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

	// calculo da cor
	float t, h1;
	float c = (mesh_data.angle)*mesh_data.out_radius;
	float previous_c = mesh_data.pre_angle*mesh_data.d1*(1/tan(mesh_data.pre_angle/2));
	vec4 color_1, color_2;
	float prop_1, prop_2;

	if(change_color == 0){
		if(mesh_data.no_curve == 1)
			if(mesh_data.d1 == 0.0f){
				h1 = mesh_data.height;
				t = (gl_TessCoord.y * h1 + mesh_data.d1)/h1;
			}
			else{
				h1 = mesh_data.height - mesh_data.d1 + previous_c/2.0f;
				t = (gl_TessCoord.y * h1 + previous_c/2.0f)/h1;
			}
		else{
			if(mesh_data.d1 == 0.0f){
				h1 = mesh_data.height - mesh_data.d2 + c/2.0f;
				t = (gl_TessCoord.y * h1/cylinder_percent)/h1;
			}	
			else{
				h1 = mesh_data.height - mesh_data.d2 + c/2.0f - mesh_data.d1 + previous_c/2.0f;
				t = (gl_TessCoord.y * h1/cylinder_percent + previous_c/2.0f)/h1;
			}
			if(is_curve == 1){
				t = ((((gl_TessCoord.y - cylinder_percent)*(1/((1-cylinder_percent)/2.0f)))*c/2.0f) + h1 - c/2.0f)/h1;
			}
		}
		prop_1 = prop[0];
		prop_2 = prop[1];
	}
	else{
		float h2;
		if(mesh_data.next_angle == 0.0f){
			h2 = mesh_data.next_height - mesh_data.d2 + c/2.0f;
			t = (((gl_TessCoord.y - cylinder_percent -((1-cylinder_percent)/2.0f))*(1/((1 - cylinder_percent)/2.0f)))*c/2.0f)/h2;
		}
		else{
			float next_radius = mesh_data.next_d2*(1/tan(mesh_data.next_angle/2));
			float c2 = mesh_data.next_angle*next_radius;
			h2 = mesh_data.next_height - mesh_data.next_d2 + c2/2.0f - mesh_data.d2 + c/2.0f;
			t = (((gl_TessCoord.y - cylinder_percent -((1-cylinder_percent)/2.0f))*(1/((1 - cylinder_percent)/2.0f)))*c/2.0f)/h2;
		}	
		prop_1 = prop[1];
		prop_2 = prop[2];	
	}

	float u = prop_1 + (prop_2 - prop_1) * t;
	int i = 0;
	while( i < textureSize(color_scale) - 1){
		vec4 a = texelFetch(color_scale, i);
		vec4 b = texelFetch(color_scale, i+1);
		if(u >= a[0] && u < b[0]){
			color_1 = vec4(a[1], a[2], a[3], 1.0f);
			color_2 = vec4(b[1], b[2], b[3], 1.0f);	
			u = (u - a[0])/(b[0] - a[0]);
			break;
		}
		else if(u > b[0] && i == textureSize(color_scale) - 2){
			color_1 = vec4(a[1], a[2], a[3], 1.0f);
			color_2 = vec4(b[1], b[2], b[3], 1.0f);	
			u = 1.0f;
			break;
		}
		i++;
	}

	v.color.r = color_1.r + (color_2.r - color_1.r) * u;
	v.color.g = color_1.g + (color_2.g - color_1.g) * u;
	v.color.b = color_1.b + (color_2.b - color_1.b) * u;
	v.color.a = color_1.a + (color_2.a - color_1.a) * u;

	gl_Position = mvp * vpos;
}