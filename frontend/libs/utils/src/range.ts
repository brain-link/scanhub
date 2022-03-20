export function range(startStop: number, stop?: number, step?: number) {
  const start = stop !== undefined ? startStop : 0
  const stop_ = stop ?? startStop
  const step_ = step ?? 1
  const length = Math.floor((stop_ - start) / step_)
  return new Array(length).fill(0).map((_, i) => start + i * step_)
}
