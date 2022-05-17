import React, { useCallback, useRef, useLayoutEffect } from 'react'
import { useRegl } from './contexts/ReglInstanceContext'
import type { HTMLDrawCmd } from './DrawCmd'
import { recursiveRender } from './DrawCmd'
import { RequestRedrawContext } from './contexts/RequestRedrawContext'
import type REGL from 'regl'

type Props = {
  run?: boolean
}

const RenderScope: React.FC<Props> = ({
  children,
  run,
}) => {
  const regl = useRegl()
  const cmdContainerRef = useRef<HTMLDivElement>(null)
  const needsRedrawRef = useRef<boolean>(true)
  const requestRedraw = useCallback(() => { needsRedrawRef.current = true }, [])

  useLayoutEffect(() => {
    if (!run) return

    let prevCtx: Partial<REGL.DefaultContext> = {}
    const frame = regl?.frame(ctx => {
      const resized = (
        prevCtx.viewportWidth != ctx.viewportWidth ||
        prevCtx.viewportHeight != ctx.viewportHeight ||
        prevCtx.pixelRatio != ctx.pixelRatio
      )
      if (resized || needsRedrawRef.current) {
        prevCtx = { ...ctx }
        // set to false before recursive render since
        // some commands might want to set this to true
        // again through react context while rendering
        needsRedrawRef.current = false
        cmdContainerRef.current?.childNodes.forEach(ch => {
          recursiveRender(ch as HTMLDrawCmd)
        })
      }
    })
    return () => {
      // cancelation might fail because
      // this effect will rerun in response to regl
      // being destroyed (animation frame will have
      // already been canceled and it can't be canceled twice).
      // Therefore, we should swallow the error if it arises.
      try {
        frame?.cancel()
      } catch {
        // still inform the user about it
        // eslint-disable-next-line no-console
        console.warn('Failed to cancel animation frame.')
      }
    }
  }, [regl, cmdContainerRef, needsRedrawRef, run])

  return (
    <div ref={cmdContainerRef}>
      <RequestRedrawContext.Provider value={requestRedraw}>
        {children}
      </RequestRedrawContext.Provider>
    </div>
  )
}

export default React.memo(RenderScope) as typeof RenderScope
