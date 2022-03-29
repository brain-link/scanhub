import { glsl } from '../glsl'

/** 0-1 random */
export const random = glsl`
float random(float x){
  return fract(sin(x * 12.9898) * 43758.5453);
}
`
