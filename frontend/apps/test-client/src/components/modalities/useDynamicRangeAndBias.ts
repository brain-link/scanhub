import { useEffect, useState } from 'react'
import { mouse } from 'input'
import { clamp } from 'utils'

const dynamicRangeSensitivity = 0.002
const biasSensitivity = 0.002

export function useDynamicRangeAndBias(ref: React.RefObject<HTMLDivElement>) {
  const [dynamicRange, setDynamicRange] = useState(1)
  const [bias, setBias] = useState(0)

  useEffect(
    () => {
      const element = ref.current
      if (element) {
        return mouse({
          element,
          onUpdate: mouse => {
            if (mouse.button.right === 'down') {
              setDynamicRange(1)
              setBias(0)
            }
            if (mouse.button.left === 'down') {
              setDynamicRange(prev => clamp(
                prev + mouse.dpos[0] * dynamicRangeSensitivity,
                0.01, 2
              ))
              setBias(prev => clamp(
                prev + mouse.dpos[1] * biasSensitivity,
                -1, 1
              ))
            }
          },
        })
      }
    },
    [ref]
  )

  return {
    dynamicRange,
    bias,
  }
}
