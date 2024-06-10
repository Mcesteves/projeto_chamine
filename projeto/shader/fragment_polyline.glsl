#version 410

const float ka = 1.0f;
const vec4 ma = vec4(0.5f, 0.5f, 0.5f, 1.0f);
const vec4 md = vec4(0.7f, 0.7f, 0.7f, 1.0f);
const vec4 ms = vec4(0.8f, 0.8f, 0.8f, 1.0f);


in vec3 out_t;
in vec3 out_l;
out vec4 color;

void main(){

	float lt = dot(normalize(out_t), normalize(out_l));
	float ln = sqrt(1 - pow(lt, 2));

	color = vec4(1.0f, 0.0f, 0.0f, 1.0f)*(ka * ma + md * max(0, ln));
	//color = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}