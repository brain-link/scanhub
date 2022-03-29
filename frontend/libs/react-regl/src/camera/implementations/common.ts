import { glsl } from 'shaders'

export const linearCameraGLSL = glsl`
  uniform mat4 view, projection;
  vec4 cameraTransform(vec4 pos) {
    return projection * view * pos;
  }
`
