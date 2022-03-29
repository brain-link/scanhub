export type ButtonState = 'up' | 'down'
export type ButtonStateChange = 'clicked' | 'released' | 'none'

export type BoundaryState = 'in' | 'out'
export type BoundaryStateChange = 'enter' | 'exit' | 'none'

export type MouseState = {
  element: HTMLElement
  pos: [number, number]
  scrollDelta: [number, number]
  button: {
    left: ButtonState
    right: ButtonState
    middle: ButtonState
    back: ButtonState
    forward: ButtonState
  }
  bounds: BoundaryState
}

export type MouseStateChange = {
  dpos: [number, number]
  buttonChange: {
    left: ButtonStateChange
    right: ButtonStateChange
    middle: ButtonStateChange
    back: ButtonStateChange
    forward: ButtonStateChange
  }
  boundsChange: BoundaryStateChange
}
