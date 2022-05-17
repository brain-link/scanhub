import { glsl } from '../glsl'

/**
 * To be used with interpolation functions when boundary was extended
 * to account for boundary conditions.
 * ```
 * vec2 uvInsetBoundary(vec2 uv, vec2 texSize, vec2 extCount?);
 * ```
 *
 * Arguments:
 *  uv: coords to transform
 *  texSize: total texture size
 *  extCount: number of rows/cols extended
 */
export const uvInsetBoundary = glsl`
  vec2 uvInsetBoundary(vec2 uv, vec2 texSize, vec2 extCount) {
    vec2 offset = extCount / texSize;
    return offset + uv * (1.0 - 2.0 * offset);
  }

  vec2 uvInsetBoundary(vec2 uv, vec2 texSize) {
    return uvInsetBoundary(uv, texSize, vec2(2.0));
  }
`
