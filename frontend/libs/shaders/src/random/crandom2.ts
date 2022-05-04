import { glsl } from '../glsl'

/** Centered random */
export const crandom2 = glsl`
float crandom2(vec2 uv){
  return 2.0 * fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453) - 1.0;
}
`
