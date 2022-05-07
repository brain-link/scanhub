import React from 'react'
import { useRef, useLayoutEffect } from 'react'
import type REGL from 'regl'
import { useRequestRedraw } from './contexts/RequestRedrawContext'

type DrawCmdProps = {
  cmd?: REGL.DrawCommand | undefined
  bodyfn?: REGL.CommandBodyFn | undefined
  uniforms?: REGL.Uniforms | undefined
}

export type HTMLDrawCmd = HTMLDivElement & DrawCmdProps

export function recursiveRender(cmdEl: HTMLDrawCmd | null) {
  const props = cmdEl?.uniforms ?? {}
  if (cmdEl) {
    if (cmdEl.bodyfn) {
      if (cmdEl.cmd) {
        cmdEl.cmd(cmdEl.bodyfn)
      } else {
        // @ts-expect-error TODO fix types
        cmdEl.bodyfn()
      }
    }
    if (cmdEl.childNodes.length === 0) {
      cmdEl.cmd?.(props)
    } else {
      cmdEl.cmd?.(props, () => {
        cmdEl.childNodes.forEach(el => {
          recursiveRender(el as HTMLDrawCmd)
        })
      })
    }
  }
}

const DrawCmd: React.FC<DrawCmdProps> = ({
  children,
  cmd,
  bodyfn,
  uniforms,
}) => {
  const ref = useRef<HTMLDrawCmd>(null)
  const requestRedraw = useRequestRedraw()
  useLayoutEffect(
    () => {
      const element = ref.current
      if (element) {
        element.cmd = cmd
        element.bodyfn = bodyfn
        element.uniforms = uniforms
        requestRedraw()
      }
    },
    [ref, cmd, bodyfn, requestRedraw, uniforms]
  )
  return (
    <div ref={ref}>
      {children}
    </div>
  )
}

export default React.memo(DrawCmd) as typeof DrawCmd
