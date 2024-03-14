#version 410

const float ka = 0.2f;
const vec4 ma = vec4(0.5f, 0.5f, 0.5f, 1.0f);
const vec4 md = vec4(1.0f, 1.0f, 1.0f, 1.0f);
const vec4 ms = vec4(1.0f, 1.0f, 1.0f, 1.0f);
const float shi = 64.0f;

in data {
	vec3 neye;
	vec3 veye;
	vec3 light;
} f;

out vec4 color;

void main(){
	vec3 vnorm = normalize(-f.veye);
	vec3 nnorm = normalize(f.neye);
	vec3 lnorm = normalize(f.light);
	float ndotl = dot(nnorm, lnorm);

	color = (ma * ka + md * max(0, ndotl));
	if(ndotl > 0){
		vec3 refl = normalize(reflect(-lnorm, nnorm));
		color += ms * pow ( max (0 , dot ( refl , vnorm)) , shi);
	}
}