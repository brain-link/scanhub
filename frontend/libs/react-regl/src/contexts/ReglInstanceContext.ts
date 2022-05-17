import { createContext, useContext } from 'react'
import type { Regl } from 'regl'

export const ReglInstanceContext = createContext<Regl | undefined>(undefined)

export function useRegl() {
  return useContext(ReglInstanceContext)
}
