import React, { useEffect, useMemo, useState } from 'react'
import { DrawCmd, useRegl, useViewport } from '..'
import { CameraContext, CameraTransformContext } from './Contexts'
import type { CameraImplementation } from './types'
import { mouse } from 'input'

export type CameraProps<P> = {
  implementation: CameraImplementation<P>
  interactive?: boolean
  props?: Partial<P>
  setProps?: React.Dispatch<React.SetStateAction<Partial<P>>>
}

function Camera<T extends React.PropsWithChildren<CameraProps<P>>, P>(
  {
    children,
    implementation: { ctor, mouseHandler },
    interactive = true,
    props: maybeProps,
    setProps: maybeSetProps,
  }: T
) {
  const regl = useRegl()
  const { viewportWidth = 1, viewportHeight = 1 } = useViewport() ?? {}
  const [localProps, localSetProps] = useState<Partial<P>>(maybeProps ?? {})

  // if setProps is not provided, use local state
  const [props, setProps] = maybeSetProps ?
    [maybeProps, maybeSetProps] :
    [localProps, localSetProps]

  const aspect = viewportWidth / viewportHeight
  const { type, glsl, uniforms, transform } = useMemo(
    () => ctor({ ...(props as P), aspect }),
    [aspect, ctor, props]
  )

  useEffect(
    () => {
      return interactive && regl?._gl.canvas ? mouse({
        element: regl._gl.canvas as HTMLCanvasElement,
        onUpdate: mouse => setProps(props => mouseHandler(mouse, props)),
      }) : undefined
    },
    [interactive, mouseHandler, regl?._gl.canvas, setProps]
  )

  const uniformscmd = useMemo(
    () => regl?.({ uniforms: { view: regl.prop('view'), projection: regl.prop('projection') } }),
    [regl]
  )
  const cameraContext = useMemo(() => ({ type, glsl }), [glsl, type])
  return (
    <CameraContext.Provider value={cameraContext}>
      <CameraTransformContext.Provider value={transform}>
        <DrawCmd cmd={uniformscmd} uniforms={uniforms}>
          {children}
        </DrawCmd>
      </CameraTransformContext.Provider>
    </CameraContext.Provider>
  )
}

export default React.memo(Camera) as typeof Camera
