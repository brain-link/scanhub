import { createContext, useContext } from 'react'

export type ViewportContextState = {
  pixelRatio: number
  viewportHeight: number
  viewportWidth: number
}

export const ViewportContext = createContext<ViewportContextState | undefined>(undefined)

export function useViewport() {
  return useContext(ViewportContext)
}
