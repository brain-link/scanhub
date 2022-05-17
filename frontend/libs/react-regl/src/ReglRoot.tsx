import React from 'react'
import { useRef, useLayoutEffect, useState } from 'react'
import type { Regl } from 'regl'
import REGL from 'regl'
import { ReglInstanceContext } from './contexts/ReglInstanceContext'
import RenderScope from './RenderScope'
import Viewport from './commands/Viewport'

const defaultAttributes: REGL.InitializationOptions['attributes'] = {
  alpha: false,
  preserveDrawingBuffer: true,
}
const defaultExtensions: REGL.InitializationOptions['extensions'] = []

export type Props = {
  attributes?: REGL.InitializationOptions['attributes']
  extensions?: REGL.InitializationOptions['extensions']
  pixelRatio?: REGL.InitializationOptions['pixelRatio']
  run?: boolean
}

const stretch: React.CSSProperties = {
  position: 'absolute',
  width: '100%',
  height: '100%',
}

/**
 * Root `react-regl` component. It handles `regl` creation
 * and exposes the `regl` instance through ReglInstanceContext
 * that you can access using `useRegl()` hook.
 * ```tsx
 * // inside a component
 * const regl = useRegl();
 * const cmd = useMemo(()=>regl?.({...}), [...]);
 * return <DrawCmd cmd={cmd} />;
 * ```
 */
const ReglRoot: React.FC<Props> = ({
  children,
  attributes,
  extensions,
  pixelRatio = devicePixelRatio,
  run = true,
}) => {
  const containerRef = useRef<HTMLDivElement>(null)
  const [reglInstance, setReglInstance] = useState<Regl>()

  useLayoutEffect(
    () => {
      if (containerRef.current) {
        const regl = REGL({
          container: containerRef.current,
          attributes: { ...defaultAttributes, ...attributes },
          pixelRatio,
          extensions: extensions ?? defaultExtensions,
        })
        // eslint-disable-next-line no-console
        console.info('Recreated context.')
        setReglInstance(() => regl)
        // cleanup
        return () => {
          regl.destroy()
          // force remove context
          // so that we don't hit max contexts
          // when rerendering a lot of times
          regl._gl.getExtension('WEBGL_lose_context')?.loseContext()
        }
      }
    },
    [attributes, containerRef, extensions, pixelRatio]
  )

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      height: '100%',
    }}>
      <div ref={containerRef} style={stretch}>
        {/** Regl renders canvas here */}
      </div>
      <ReglInstanceContext.Provider value={reglInstance}>
        <RenderScope run={run}>
          <Viewport>
            {children}
          </Viewport>
        </RenderScope>
      </ReglInstanceContext.Provider>
    </div>
  )
}

export default React.memo(ReglRoot) as typeof ReglRoot
