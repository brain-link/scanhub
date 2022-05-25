import { glsl } from '../glsl'
import type { WrapFn } from './types'

/**
 * (Almost) Drop in replacement for texture2D with a crucial
 * difference that textureBilinear needs a third argument `texSize`:
 * ```glsl
 * vec4 textureBilinear(sampler2D sampler, vec2 uv, vec2 texSize);
 * ```
 * Optional wrapUv parameter is for modifying uv coordinates just
 * before sampling the texture (for spherical wrap-around for example).
 *
 * NOTE: linear texture sampling is natively supported by WebGL, however
 * there is a limitation. If you want a repeated texture (for spherical wrap)
 * you must provide a power-of-2 texture. Since in general textures are NPOT,
 * manual linear sampling is done.
 */
export const textureBilinear = (wrapUv?: WrapFn) => glsl`
  vec4 textureBilinear(sampler2D sampler, vec2 uv, vec2 texSize) {
    vec2 texelSize = 1.0 / texSize;
    vec2 uvPx = uv * texSize;
    vec2 uvCenter = floor(uvPx - 0.5) + 0.5;
    vec2 uvFract = uvPx - uvCenter;

    uv = uvCenter * texelSize;
    ${wrapUv?.('uv')}
    vec4 p0q0 = texture2D(sampler, uv);

    uv = (uvCenter + vec2(1, 0)) * texelSize;
    ${wrapUv?.('uv')}
    vec4 p1q0 = texture2D(sampler, uv);

    uv = (uvCenter + vec2(0, 1)) * texelSize;
    ${wrapUv?.('uv')}
    vec4 p0q1 = texture2D(sampler, uv);

    uv = (uvCenter + vec2(1, 1)) * texelSize;
    ${wrapUv?.('uv')}
    vec4 p1q1 = texture2D(sampler, uv);

    vec4 pInterp_q0 = mix(p0q0, p1q0, uvFract.x); // Interpolates top row in X direction.
    vec4 pInterp_q1 = mix(p0q1, p1q1, uvFract.x); // Interpolates bottom row in X direction.

    return mix(pInterp_q0, pInterp_q1, uvFract.y); // Interpolate in Y direction.
  }
`
