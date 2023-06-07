// Copyright (C) 2023, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
// SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial

// DICOM.tsx is responsible for rendering the DICOM modality.

import type { ModalityProps } from './types'
import { Camera, camera2d, camera3d, Clear, DrawCmd, ReglRoot, useCamera, useRegl } from 'react-regl'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { glsl, hsl2rgb } from 'shaders'
import { deferred } from 'utils'
import type { Regl, Vec4, Vec3 } from 'regl'
import { useDynamicRangeAndBias } from './useDynamicRangeAndBias'
import { CCard, CContainer, CCardSubtitle, CCardTitle, CCol, CRow } from '@coreui/react'

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
        // weird <{}...> to silence typescript
        texture: regl.prop<{ texture: unknown }, 'texture'>('texture'),
        inverseDynamicRange: regl.prop<{ inverseDynamicRange: unknown }, 'inverseDynamicRange'>('inverseDynamicRange'),
        bias: regl.prop<{ bias: unknown }, 'bias'>('bias'),
        up: regl.prop<{ up: unknown }, 'up'>('up'),
        right: regl.prop<{ right: unknown }, 'right'>('right'),
        center: regl.prop<{ center: unknown }, 'center'>('center'),
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
  const { dynamicRange, bias } = useDynamicRangeAndBias(ref)
  const [xyPlaneCenter, setXYPlaneCenter] = useState(0)
  const [yzPlaneCenter, setYZPlaneCenter] = useState(0)
  const [xzPlaneCenter, setXZPlaneCenter] = useState(0)
  return (
    <div>
      <CCardTitle> { recordingId } </CCardTitle>

      <CRow className='mb-3 mt-3'>
        <CCol md={4} className="align-middle">
          <CCard className='align-middle p-2'>
            <CCardSubtitle className='mb-2'>XY Plane Offset</CCardSubtitle>
            <input
              type='range'
              min={-1} max={1} step={1e-4}
              value={xyPlaneCenter}
              onChange={ev => setXYPlaneCenter(ev.target.valueAsNumber)}
              width="100%"
            />
          </CCard>
        </CCol>
        <CCol md={4}>
          <CCard className='align-middle p-2'>
            <CCardSubtitle className='mb-2'>YZ Plane Offset</CCardSubtitle>
            <input
              type='range'
              min={-1} max={1} step={1e-4}
              value={yzPlaneCenter}
              onChange={ev => setYZPlaneCenter(ev.target.valueAsNumber)}
            />
          </CCard>
        </CCol>
        <CCol md={4}>
          <CCard className='p-2'>
            <CCardSubtitle className='mb-2'>XZ Plane Offset</CCardSubtitle>
            <input
              type='range'
              min={-1} max={1} step={1e-4}
              value={xzPlaneCenter}
              onChange={ev => setXZPlaneCenter(ev.target.valueAsNumber)}
            />
          </CCard>

        </CCol>
      </CRow>
      

      <CContainer className='p-0'>
        <CRow className='mb-2'>
          <CCol md={6}>
            <CCard style={{ height: '20rem'}}>
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
            </CCard>
          </CCol>
          <CCol md={6}>
            <CCard style={{ height: '20rem'}}>
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
            </CCard>
          </CCol>
        </CRow>
        <CRow>
          <CCol md={6}>
            <CCard style={{ height: '20rem'}}>
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
            </CCard>
          </CCol>
          <CCol md={6}>
            <CCard style={{ height: '20rem'}}>
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
            </CCard>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}
