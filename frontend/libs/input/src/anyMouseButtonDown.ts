import type { MouseState } from './types'

export function anyMouseButtonDown(state: MouseState): boolean {
  return [
    state.button.left,
    state.button.right,
    state.button.middle,
    state.button.back,
    state.button.forward,
  ].some(v => v === 'down')
}
