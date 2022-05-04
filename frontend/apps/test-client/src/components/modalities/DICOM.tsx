import type { ModalityProps } from './types'
import { Camera, camera2d, camera3d, Clear, DrawCmd, ReglRoot, useCamera, useRegl } from 'react-regl'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { glsl, hsl2rgb } from 'shaders'
import { deferred } from 'utils'
import type { Regl, Vec4, Vec3 } from 'regl'

function imageFromUrl(url: string): Promise<HTMLImageElement> {
  const { promise, resolve } = deferred<HTMLImageElement>()
  const image = new Image()
  image.src = url
  image.addEventListener('load', () => resolve(image))
  return promise
}

async function textureFromUrl(regl: Regl, url: string) {
  const image = await imageFromUrl(url)
  return regl.texture({
    data: image,
    flipY: true,
    mag: 'nearest',
  })
}

function useAsyncResource<T>(resourcefn: () => Promise<T>) {
  const [result, setResult] = useState<T>()
  useEffect(
    () => {
      resourcefn().then(res => {
        setResult(() => res)
      })
    },
    [resourcefn]
  )
  return result
}

type PlaneProps = {
  url: string
  dynamicRange: number
  bias: number
  up?: Vec3
  right?: Vec3
  center?: Vec3
}

const origin: Vec3 = [0, 0, 0]
const xAxis: Vec3 = [1, 0, 0]
const yAxis: Vec3 = [0, 1, 0]
const zAxis: Vec3 = [0, 0, 1]

function Plane({
  url,
  dynamicRange,
  bias,
  up = yAxis,
  right = xAxis,
  center = origin,
}: PlaneProps) {
  const regl = useRegl()
  const camera = useCamera()
  const texture = useAsyncResource(
    useCallback(
      async () => regl ?
        await textureFromUrl(regl, url) :
        undefined,
      [regl, url]
    )
  )
  const uniforms = useMemo(
    () => texture ? {
      texture,
      inverseDynamicRange: 1 / dynamicRange,
      bias,
      up,
      right,
      center,
    } : undefined,
    [bias, center, dynamicRange, right, texture, up]
  )
  const cmd = useMemo(
    () => regl && camera?.glsl && texture ? regl({
      vert: glsl`
        precision mediump float;
        ${camera.glsl}
        uniform vec3 up, right, center;
        attribute vec2 uv;

        varying vec2 vUv;

        void main() {
          vUv = uv;
          vec3 position = (uv.x-0.5) * right + (uv.y-0.5) * up + center;
          gl_Position = cameraTransform(vec4(position, 1.0));
        }
      `,
      frag: glsl`
        precision mediump float;
        uniform float inverseDynamicRange;
        uniform float bias;
        uniform sampler2D texture;
        varying vec2 vUv;

        ${hsl2rgb}

        void main() {
          float value = texture2D(texture, vUv).x;
          value = inverseDynamicRange * (value - bias);
          // vec3 color = hsl2rgb(value, 0.8, 0.5);
          vec3 color = vec3(value);
          gl_FragColor = vec4(color, 1.0);
        }
      `,
      attributes: {
        uv: [
          [0, 0],
          [1, 0],
          [0, 1],
          [1, 1],
        ],
      },
      uniforms: {
        texture: regl.prop('texture'),
        inverseDynamicRange: regl.prop('inverseDynamicRange'),
        bias: regl.prop('bias'),
        up: regl.prop('up'),
        right: regl.prop('right'),
        center: regl.prop('center'),
      },
      primitive: 'triangle strip',
      count: 4,
    }) : undefined,
    [camera?.glsl, regl, texture]
  )
  return <DrawCmd cmd={cmd} uniforms={uniforms} />
}

const clearColor: Vec4 = [0.2, 0.2, 0.2, 1]

export function DICOM({
  recordingId,
}: ModalityProps) {
  const ref = useRef<HTMLDivElement>(null)
  const [dynamicRange, setDynamicRange] = useState(1)
  const [bias, setBias] = useState(0)
  const [xyPlaneCenter, setXYPlaneCenter] = useState(0)
  const [yzPlaneCenter, setYZPlaneCenter] = useState(0)
  const [xzPlaneCenter, setXZPlaneCenter] = useState(0)
  return (
    <div>
      <ul>
        <li>
          Dynamic range:
          <input
            type='range'
            min={0.01} max={2} step={1e-4}
            value={dynamicRange}
            onChange={ev => setDynamicRange(ev.target.valueAsNumber)}
          />{dynamicRange}
        </li>
        <li>
          Bias:
          <input
            type='range'
            min={-1} max={1} step={1e-4}
            value={bias}
            onChange={ev => setBias(ev.target.valueAsNumber)}
          />{bias}
        </li>
        <li>
          XY Plane Offset:
          <input
            type='range'
            min={-1} max={1} step={1e-4}
            value={xyPlaneCenter}
            onChange={ev => setXYPlaneCenter(ev.target.valueAsNumber)}
          />
        </li>
        <li>
          YZ Plane Offset:
          <input
            type='range'
            min={-1} max={1} step={1e-4}
            value={yzPlaneCenter}
            onChange={ev => setYZPlaneCenter(ev.target.valueAsNumber)}
          />
        </li>
        <li>
          XZ Plane Offset:
          <input
            type='range'
            min={-1} max={1} step={1e-4}
            value={xzPlaneCenter}
            onChange={ev => setXZPlaneCenter(ev.target.valueAsNumber)}
          />
        </li>
      </ul>
      <div ref={ref} className="grid col-2 gap-2" style={{ width: '100%', height: '900px' }}>
        <ReglRoot>
          <Clear color={clearColor} />
          <Camera implementation={camera2d}>
            <Plane
              url='./mri_image.jpg'
              dynamicRange={dynamicRange}
              bias={bias}
            />
          </Camera>
        </ReglRoot>
        <ReglRoot>
          <Clear color={clearColor} />
          <Camera implementation={camera2d}>
            <Plane
              url='./mri_image.jpg'
              dynamicRange={dynamicRange}
              bias={bias}
            />
          </Camera>
        </ReglRoot>
        <ReglRoot>
          <Clear color={clearColor} />
          <Camera implementation={camera2d}>
            <Plane
              url='./mri_image.jpg'
              dynamicRange={dynamicRange}
              bias={bias}
            />
          </Camera>
        </ReglRoot>
        <ReglRoot>
          <Clear color={clearColor} />
          <Camera implementation={camera3d}>
            <Plane
              url='./mri_image.jpg'
              dynamicRange={dynamicRange}
              bias={bias}
              center={[0, 0, xyPlaneCenter]}
            />
            <Plane
              url='./mri_image.jpg'
              dynamicRange={dynamicRange}
              bias={bias}
              up={yAxis}
              right={zAxis}
              center={[yzPlaneCenter, 0, 0]}
            />
            <Plane
              url='./mri_image.jpg'
              dynamicRange={dynamicRange}
              bias={bias}
              up={xAxis}
              right={zAxis}
              center={[0, xzPlaneCenter, 0]}
            />
          </Camera>
        </ReglRoot>
      </div>
    </div>
  )
}
