import { glsl } from '../glsl'

/** Centered random */
export const crandom = glsl`
float crandom(float x){
  return 2.0 * fract(sin(x * 12.9898) * 43758.5453) - 1.0;
}
`
