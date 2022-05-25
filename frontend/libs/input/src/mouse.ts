import type {
  BoundaryState,
  BoundaryStateChange,
  ButtonState,
  ButtonStateChange,
  MouseState,
  MouseStateChange,
} from './types'
import { anyMouseButtonDown } from './anyMouseButtonDown'

/** Given previous and next button state, compute button state change. */
function buttonStateChange(
  prev: ButtonState,
  next?: ButtonState
): ButtonStateChange {
  if (next === undefined) return 'none'
  switch (`${prev}>${next}` as const) {
    case 'up>up': return 'none'
    case 'down>down': return 'none'
    case 'down>up': return 'released'
    case 'up>down': return 'clicked'
  }
}

/** Given previous and next boundary state, compute boundary state change. */
function boundaryStateChange(
  prev: BoundaryState,
  next?: BoundaryState
): BoundaryStateChange {
  if (next === undefined) return 'none'
  switch (`${prev}>${next}` as const) {
    case 'in>in': return 'none'
    case 'out>out': return 'none'
    case 'in>out': return 'exit'
    case 'out>in': return 'enter'
  }
}

/** Given previous and next mouse state, compute mouse state change. */
function mouseStateChange(
  prev: MouseState,
  next: Partial<MouseState>
): MouseStateChange {
  return {
    dpos: next.pos ? [next.pos[0] - prev.pos[0], next.pos[1] - prev.pos[1]] : [0, 0],
    buttonChange: {
      left: buttonStateChange(prev.button.left, next.button?.left),
      right: buttonStateChange(prev.button.right, next.button?.right),
      middle: buttonStateChange(prev.button.middle, next.button?.middle),
      back: buttonStateChange(prev.button.back, next.button?.back),
      forward: buttonStateChange(prev.button.forward, next.button?.forward),
    },
    boundsChange: boundaryStateChange(prev.bounds, next.bounds),
  }
}

type Props = {
  onUpdate?: (state: MouseState & MouseStateChange) => void
  element?: HTMLElement
  preventDefault?: boolean
}

/**
 * Hooks up event handlers to a specific element on the page with the
 * corresponding `onUpdate` handler. Return value is a cleanup function
 * to be returned in `useEffect` for example.
 */
export function mouse(
  {
    element = document.body,
    onUpdate,
    preventDefault = true,
  }: Props
) {
  const state: MouseState & MouseStateChange = {
    element,
    pos: [0, 0],
    dpos: [0, 0],
    scrollDelta: [0, 0],
    button: {
      left: 'up',
      right: 'up',
      middle: 'up',
      back: 'up',
      forward: 'up',
    },
    buttonChange: {
      left: 'none',
      right: 'none',
      middle: 'none',
      back: 'none',
      forward: 'none',
    },
    bounds: element.matches(':hover') ? 'in' : 'out',
    boundsChange: 'none',
  }

  function setState(diff: Partial<MouseState>) {
    Object.assign(state, diff, mouseStateChange(state, diff))
    onUpdate?.(state)
    // scroll delta should not be preserved
    state.scrollDelta = [0, 0]
  }

  /** Shorthand for checking bounds and preventing default if specified */
  function checkBoundsPreventDefault<T extends Event>(action: (ev: T) => void) {
    return (ev: T) => {
      if (state.bounds === 'in' || anyMouseButtonDown(state)) {
        preventDefault && ev.preventDefault()
        action(ev)
      }
    }
  }

  const pointermove = (ev: MouseEvent) => {
    // NOTES:
    // - since this event is registered on window, it's (x, y) will be
    //   in relation to the window.
    // - getBoundingClientRect returns floating point values, therefore it is
    //   necessary to round them down using Math.floor
    const { left, top, width, height } = state.element.getBoundingClientRect()
    const { x, y } = ev
    const offsetX = x - Math.floor(left)
    const offsetY = y - Math.floor(top)
    const isInside = (
      offsetX >= 0 && offsetY >= 0 &&
      offsetX < Math.floor(width) && offsetY < Math.floor(height)
    )
    setState({
      pos: [offsetX, offsetY],
      bounds: isInside ? 'in' : 'out',
    })
  }

  const pointerupdown = checkBoundsPreventDefault((ev: MouseEvent) => {
    setState({
      button: {
        left: ev.buttons & 1 ? 'down' : 'up',
        right: ev.buttons & 2 ? 'down' : 'up',
        middle: ev.buttons & 4 ? 'down' : 'up',
        back: ev.buttons & 8 ? 'down' : 'up',
        forward: ev.buttons & 16 ? 'down' : 'up',
      },
    })
  })

  const wheel = checkBoundsPreventDefault((ev: WheelEvent) => {
    setState({ scrollDelta: [ev.deltaX, ev.deltaY] })
  })

  const contextmenu = checkBoundsPreventDefault(() => { })

  window.addEventListener('pointermove', pointermove)
  window.addEventListener('pointerup', pointerupdown)
  element.addEventListener('pointerdown', pointerupdown)
  element.addEventListener('wheel', wheel, { passive: false })
  element.addEventListener('contextmenu', contextmenu)

  // return how to cleanup
  return () => {
    window.removeEventListener('pointermove', pointermove)
    window.removeEventListener('pointerup', pointerupdown)
    element.removeEventListener('pointerdown', pointerupdown)
    element.removeEventListener('wheel', wheel)
    element.removeEventListener('contextmenu', contextmenu)
  }
}
