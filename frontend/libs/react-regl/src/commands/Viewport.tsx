import React from 'react'
import { useMemo, useCallback, useState } from 'react'
import { useRegl, DrawCmd } from '..'
import type { BoundingBox, DefaultContext, MaybeNestedDynamic } from 'regl'
import type { ViewportContextState } from '../contexts/ViewportContext'
import { ViewportContext } from '../contexts/ViewportContext'

const defaultWidth = (ctx: DefaultContext) => ctx.drawingBufferWidth
const defaultHeight = (ctx: DefaultContext) => ctx.drawingBufferHeight

type Props = MaybeNestedDynamic<BoundingBox, DefaultContext, Record<string, unknown>>;

const Viewport: React.FC<Props> = ({
  children,
  x = 0,
  y = 0,
  width = defaultWidth,
  height = defaultHeight,
}) => {
  const regl = useRegl()
  const [viewportWidth, setViewportWidth] = useState<number>()
  const [viewportHeight, setViewportHeight] = useState<number>()
  const [pixelRatio, setPixelRatio] = useState<number>()
  const viewport = useMemo<ViewportContextState | undefined>(
    () => pixelRatio !== undefined && viewportHeight !== undefined && viewportWidth !== undefined ? ({
      pixelRatio,
      viewportHeight,
      viewportWidth,
    }) : undefined,
    [pixelRatio, viewportHeight, viewportWidth]
  )
  const uniforms = useMemo(
    () => regl?.({
      viewport: {
        // types are wrong here in regl?
        x: x as number,
        y: y as number,
        width: width as number,
        height: height as number,
      },
    }),
    [height, regl, width, x, y]
  )
  const stateUpdater = useCallback(
    (ctx: DefaultContext) => {
      setPixelRatio(ctx.pixelRatio)
      setViewportWidth(ctx.viewportWidth)
      setViewportHeight(ctx.viewportHeight)
    },
    []
  )
  return (
    <ViewportContext.Provider value={viewport}>
      <DrawCmd cmd={uniforms} bodyfn={stateUpdater}>
        {children}
      </DrawCmd>
    </ViewportContext.Provider>
  )
}

export default React.memo(Viewport) as typeof Viewport
