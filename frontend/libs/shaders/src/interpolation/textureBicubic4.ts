import { glsl } from '../glsl'

/**
 * (Almost) Drop in replacement for texture2D with a crucial
 * difference that textureBicubic4 needs a third argument `texSize`:
 * ```glsl
 * vec4 textureBicubic4(sampler2D sampler, vec2 texCoords, vec2 texSize);
 * ```
 *
 * NOTE: This is NOT an interpolative operation, rather approximative.
 */
export const textureBicubic4 = glsl`

vec4 _cubic_(float v){
  vec4 n = vec4(1.0, 2.0, 3.0, 4.0) - v;
  vec4 s = n * n * n;
  float x = s.x;
  float y = s.y - 4.0 * s.x;
  float z = s.z - 4.0 * s.y + 6.0 * s.x;
  float w = 6.0 - x - y - z;
  return vec4(x, y, z, w) * (1.0/6.0);
}

vec4 textureBicubic4(sampler2D sampler, vec2 texCoords, vec2 texSize) {
  vec2 invTexSize = 1.0 / texSize;
  texCoords = texCoords * texSize - 0.5;
  vec2 fxy = fract(texCoords);
  texCoords -= fxy;

  vec4 xcubic = _cubic_(fxy.x);
  vec4 ycubic = _cubic_(fxy.y);

  vec4 c = texCoords.xxyy + vec2 (-0.5, +1.5).xyxy;

  vec4 s = vec4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
  vec4 offset = c + vec4 (xcubic.yw, ycubic.yw) / s;

  offset *= invTexSize.xxyy;

  vec4 sample0 = texture2D(sampler, offset.xz);
  vec4 sample1 = texture2D(sampler, offset.yz);
  vec4 sample2 = texture2D(sampler, offset.xw);
  vec4 sample3 = texture2D(sampler, offset.yw);

  float sx = s.x / (s.x + s.y);
  float sy = s.z / (s.z + s.w);

  return mix(
    mix(sample3, sample2, sx), mix(sample1, sample0, sx)
  , sy);
}
`
