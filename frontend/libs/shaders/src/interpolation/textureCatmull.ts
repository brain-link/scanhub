/** Taken from https://www.codeproject.com/Articles/236394/Bi-Cubic-and-Bi-Linear-Interpolation-with-GLSL */

import { glsl } from '../glsl'
import type { WrapFn } from './types'

/**
 * (Almost) Drop in replacement for texture2D with a crucial
 * difference that textureCatmull needs a third argument `texSize`:
 * ```glsl
 * vec4 textureCatmull(sampler2D sampler, vec2 uv, vec2 texSize);
 * ```
 * Optional wrapUv parameter is for modifying uv coordinates just
 * before sampling the texture (for spherical wrap-around for example).
 */
export const textureCatmull = (wrapUv?: WrapFn) => glsl`
  float catmullrom(float x) {
    const float B = 0.0;
    const float C = 0.5;
    if(x < 0.0)
    {
      x = -x;
    }
    if(x < 1.0)
    {
      return ((12.0 - 9.0 * B - 6.0 * C) * (x * x * x) +
        (-18.0 + 12.0 * B + 6.0 *C) * (x * x) +
        (6.0 - 2.0 * B)) / 6.0;
    }
    else if(x >= 1.0 && x < 2.0)
    {
      return ((-B - 6.0 * C) * (x * x * x)
        + (6.0 * B + 30.0 * C) * (x * x) +
        (- (12.0 * B) - 48.0 * C) * x +
        8.0 * B + 24.0 * C)/ 6.0;
    }
    else
    {
      return 0.0;
    }
  }

  vec4 textureCatmull(sampler2D sampler, vec2 uv, vec2 texSize) {
    vec2 texelSize = 1.0 / texSize;
    vec2 uvPx = uv * texSize;
    vec2 uvCenter = floor(uvPx - 0.5) + 0.5;
    vec2 uvFract = uvPx - uvCenter;
    vec4 nSum = vec4(0.0, 0.0, 0.0, 0.0);
    vec4 nDenom = vec4(0.0, 0.0, 0.0, 0.0);
    for(int m = -1; m <= 2; m += 1)
    {
      for(int n = -1; n <= 2; n += 1)
      {
        vec2 mn = vec2(float(m), float(n));
        vec2 uv = (uvCenter + mn) * texelSize;
        ${wrapUv?.('uv')}
        vec4 vecData = texture2D(sampler, uv);
        float f1 = catmullrom(mn.x - uvFract.x);
        float f2 = catmullrom(-(mn.y - uvFract.y));
        nSum = nSum + (vecData * f1 * f2);
        nDenom = nDenom + (f1 * f2);
      }
    }
    return nSum / nDenom;
  }
`
