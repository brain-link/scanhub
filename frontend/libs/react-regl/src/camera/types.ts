import type { MouseState, MouseStateChange } from '../../../input/src/types'
import type { GLSL } from 'shaders'
import type { Vec4 } from 'regl'

export type CameraTransform = {
  /**
   * JS function that transforms homogeneous world coords into clip coords [-1, 1].
   */
  worldToClip: (pos: Vec4) => Vec4
  /**
   * JS function that transforms homogeneous clip coords [-1, 1] into world coords.
   */
  clipToWorld: (pos: Vec4) => Vec4
  /**
   * Distance to camera (makes sense only in 3D. For other modes it will be 0)
   */
  distanceToNearClip: (pos: Vec4) => number
}

export type CameraInstance = {
  /**
   * For example '2D' or '3D', value used for specializing
   * rendering logic for specific cameras.
   */
  type: string
  /**
   * GLSL code containing at least a function that transforms world
   * coords into screen coords:
   * ```glsl
   * vec4 cameraTransform(vec4 pos);
   * ```
   */
  glsl: GLSL
  /** Shader uniforms */
  uniforms: Record<string, unknown>
  /** JS transform functions */
  transform: CameraTransform
}

export type CameraIntrinsicProps = {
  aspect: number
}

export type CameraCtor<T> = (props: Partial<T> & CameraIntrinsicProps) => CameraInstance
export type MouseHandler<T> = (mouse: MouseState & MouseStateChange, props: Partial<T>) => Partial<T>

export type CameraImplementation<T> = {
  ctor: CameraCtor<T>
  mouseHandler: MouseHandler<T>
}
