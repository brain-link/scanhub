import { mat4, vec3, vec4, vec2 } from 'gl-matrix'
import type { CameraCtor, CameraImplementation, CameraIntrinsicProps, CameraTransform, MouseHandler } from '../types'
import { produce } from 'immer'
import type { Mat4Array } from '../../types'
import type { Vec2, Vec3 } from 'regl'
import { linearCameraGLSL } from './common'

export type Camera2DProps = {
  near: number
  far: number
  lockX: boolean
  lockY: boolean
  lockZoom: boolean
  position: Vec3
  zoom: Vec2
}

function setPropsDefaults(props: Partial<Camera2DProps>): props is Camera2DProps {
  props.near = props.near ?? -100
  props.far = props.far ?? 100
  props.lockX = props.lockX ?? false
  props.lockY = props.lockY ?? false
  props.lockZoom = props.lockZoom ?? false
  props.position = props.position ?? [0, 0, 0]
  props.zoom = props.zoom ?? [1, 1]
  return true
}

function projectionMatrix(
  { zoom, aspect, near, far }: Camera2DProps & CameraIntrinsicProps
): Mat4Array {
  const projectionMat = mat4.create()
  const [zx, zy] = zoom
  mat4.ortho(
    projectionMat,
    -0.5 * aspect / zx, 0.5 * aspect / zx,
    -0.5 / zy, 0.5 / zy,
    near, far
  )
  return [...projectionMat] as Mat4Array
}

function viewMatrix(
  { position }: Camera2DProps
): Mat4Array {
  const viewMat = mat4.create()
  mat4.translate(viewMat, mat4.create(), vec3.negate(vec3.create(), position))
  return [...viewMat] as Mat4Array
}

function transform(props: Camera2DProps & CameraIntrinsicProps): CameraTransform {
  const viewMat = viewMatrix(props)
  const projectionMat = projectionMatrix(props)
  return {
    worldToClip: pos => {
      vec4.transformMat4(pos, pos, viewMat)
      return vec4.transformMat4(pos, pos, projectionMat)
    },
    clipToWorld: () => { throw new Error('Not implemented.') },
    distanceToNearClip: () => 0,
  }
}

const mouseHandler: MouseHandler<Camera2DProps> =
  (mouse, oldProps) =>
    produce(oldProps, props => {
      if (!setPropsDefaults(props))
        throw new Error(`Unreachable code reached.`)
      const prevPos: Vec3 = [...props.position]
      const center = vec2.fromValues(
        mouse.element.offsetWidth / 2,
        mouse.element.offsetHeight / 2
      )
      const pixelToWorldCoef = vec2.fromValues(
        mouse.element.offsetHeight,
        -mouse.element.offsetHeight
      )
      vec2.mul(pixelToWorldCoef, pixelToWorldCoef, props.zoom)
      const mp = vec2.fromValues(...mouse.pos)
      const mdp = vec2.fromValues(...mouse.dpos)
      vec2.sub(mp, mp, center)
      vec2.div(mp, mp, pixelToWorldCoef)
      vec2.div(mdp, mdp, pixelToWorldCoef)
      if (mouse.button.left === 'down') {
        vec3.sub(props.position, props.position, [mdp[0], mdp[1], 0])
      }
      if (!props.lockZoom) {
        const zoomDelta = -mouse.scrollDelta[1] * 0.001
        const zoomCoef = 1 + zoomDelta
        vec2.scale(props.zoom, props.zoom, zoomCoef)
        vec3.scaleAndAdd(props.position, props.position, [...mp, 0] as vec3, 1 - 1 / zoomCoef)
      }
      // lock axes and zoom
      if (props.lockX) props.position[0] = prevPos[0]
      if (props.lockY) props.position[1] = prevPos[1]
    })

const ctor: CameraCtor<Camera2DProps> = props => {
  if (!setPropsDefaults(props))
    throw new Error(`Unreachable code reached.`)
  return ({
    type: '2D',
    glsl: linearCameraGLSL,
    uniforms: {
      view: viewMatrix(props),
      projection: projectionMatrix(props),
    },
    transform: transform(props),
  })
}

export const camera2d: CameraImplementation<Camera2DProps> = {
  ctor,
  mouseHandler,
}
