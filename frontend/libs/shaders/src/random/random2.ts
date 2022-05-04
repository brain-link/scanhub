import { glsl } from '../glsl'

/** 0-1 random */
export const random2 = glsl`
float random2(vec2 uv){
  return fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453);
}
`
