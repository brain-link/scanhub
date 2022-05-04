import React from 'react'
import { useCallback } from 'react'
import type REGL from 'regl'
import { useRegl } from '../contexts/ReglInstanceContext'
import DrawCmd from '../DrawCmd'

function Clear(props: REGL.ClearOptions): JSX.Element {
  const regl = useRegl()
  const clearcmd = useCallback(
    () => {
      regl?.clear({
        depth: 1,
        color: [0, 0, 0, 0],
        ...props,
      })
    },
    [regl, props]
  )
  return (
    <DrawCmd bodyfn={clearcmd} />
  )
}

export default React.memo(Clear) as typeof Clear
