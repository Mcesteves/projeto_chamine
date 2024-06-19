#version 410

const float ka = 1.0f;
const vec4 ma = vec4(0.3f, 0.3f, 0.3f, 1.0f);
const vec4 md = vec4(0.7f, 0.7f, 0.7f, 1.0f);
const vec4 ms = vec4(0.8f, 0.8f, 0.8f, 1.0f);
const float shi = 64.0f;

in data {
	vec3 neye;
	vec3 veye;
	vec3 light;
	vec4 color;
} f;

out vec4 color;

void main(){
	vec3 vnorm = normalize(-f.veye);
	vec3 nnorm = normalize(f.neye);
	vec3 lnorm = normalize(f.light);
	float ndotl = dot(nnorm, lnorm);

	color = f.color * (ka * ma + md * max(0, ndotl));
	if(ndotl > 0){
		vec3 refl = normalize(reflect(-lnorm, nnorm));
		color += ms * pow ( max (0 , dot ( refl , vnorm)) , shi);
	}
}