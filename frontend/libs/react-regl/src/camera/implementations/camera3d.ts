import { mat4, vec3, vec4 } from 'gl-matrix'
import type { CameraCtor, CameraImplementation, CameraIntrinsicProps, CameraTransform, MouseHandler } from '../types'
import { produce } from 'immer'
import type { Mat4Array } from '../../types'
import type { Vec3 } from 'regl'
import { linearCameraGLSL } from './common'

export type Camera3DProps = {
  /** Projection mode */
  projection: 'ortho' | 'perspective'
  /** Forward vector, [0, 0, 1] by default */
  forward: Vec3
  /** Up vector, [0, 1, 0] by default */
  up: Vec3
  /** Point around which the camera pivots */
  pivot: Vec3
  /** Rotation matrix representing rotation of the camera around the pivot */
  rotation: Mat4Array
  /** Distance to the pivot */
  distance: number
  /** Far clipping plane */
  far: number
  /** Near clipping plane */
  near: number
  /** Field of view Y in radians */
  fovy: number
  /** How much the camera is zoomed in */
  zoom: number
}

function setPropsDefaults(props: Partial<Camera3DProps>): props is Camera3DProps {
  props.projection = props.projection ?? 'perspective'
  props.near = props.near ?? 0.01
  props.far = props.far ?? 1000
  props.fovy = props.fovy ?? Math.PI / 4
  props.zoom = props.zoom ?? 1
  props.pivot = props.pivot ?? [0, 0, 0]
  props.forward = props.forward ?? [0, 0, 1]
  props.up = props.up ?? [0, 1, 0]
  props.distance = props.distance ?? 4.0
  props.rotation = props.rotation ?? [...mat4.create()] as Mat4Array
  return true
}

function projectionMatrix(
  { projection, aspect, zoom, near, far, fovy }: Camera3DProps & CameraIntrinsicProps
): Mat4Array {
  const projectionMat = mat4.create()
  switch (projection) {
    case 'ortho':
      mat4.ortho(
        projectionMat,
        -aspect / zoom,
        aspect / zoom,
        -1 / zoom,
        1 / zoom,
        near, far
      )
      break
    case 'perspective':
      mat4.perspective(
        projectionMat,
        fovy / (0.5 + zoom),
        aspect,
        near, far
      )
      break
  }
  return [...projectionMat] as Mat4Array
}

function viewMatrix(
  { forward, up, distance, pivot, rotation }: Camera3DProps
): Mat4Array {
  const viewMat = mat4.create()
  const forwardT = vec3.transformMat4(vec3.create(), forward, rotation)
  const upT = vec3.transformMat4(vec3.create(), up, rotation)
  const __0 = vec3.create()
  const pos = vec3.sub(__0, pivot, vec3.scale(__0, forwardT, distance))
  mat4.lookAt(viewMat, pos, pivot, upT)
  return [...viewMat] as Mat4Array
}

function transform(props: Camera3DProps & CameraIntrinsicProps): CameraTransform {
  const viewMat = viewMatrix(props)
  const projectionMat = projectionMatrix(props)
  return {
    worldToClip: pos => {
      vec4.transformMat4(pos, pos, viewMat)
      return vec4.transformMat4(pos, pos, projectionMat)
    },
    clipToWorld: () => { throw new Error('Not implemented.') },
    distanceToNearClip: pos => {
      const [, , z] = vec4.transformMat4(vec4.clone(pos), pos, viewMat)
      return -z
    },
  }
}

const mouseHandler: MouseHandler<Camera3DProps> =
  (mouse, oldProps) =>
    produce(oldProps, props => {
      if (!setPropsDefaults(props))
        throw new Error(`Unreachable code reached.`)
      if (mouse.button.left === 'down') {
        const sensitivity = 5
        const dx = sensitivity * mouse.dpos[0] / mouse.element.clientHeight
        const dy = sensitivity * mouse.dpos[1] / mouse.element.clientHeight
        mat4.rotateY(props.rotation, props.rotation, -dx / Math.max(1, props.zoom))
        mat4.rotateX(props.rotation, props.rotation, dy / Math.max(1, props.zoom))
      }
      const zoomDelta = -mouse.scrollDelta[1] * 0.001
      const zoomCoef = 1 + zoomDelta
      props.zoom *= zoomCoef
    })

const ctor: CameraCtor<Camera3DProps> = props => {
  if (!setPropsDefaults(props))
    throw new Error(`Unreachable code reached.`)
  return ({
    type: '3D',
    glsl: linearCameraGLSL,
    uniforms: {
      view: viewMatrix(props),
      projection: projectionMatrix(props),
    },
    transform: transform(props),
  })
}

export const camera3d: CameraImplementation<Camera3DProps> = {
  ctor,
  mouseHandler,
}
