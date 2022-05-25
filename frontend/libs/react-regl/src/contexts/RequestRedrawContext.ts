import { createContext, useContext } from 'react'

export const RequestRedrawContext = createContext<VoidFunction>(() => {
  throw new Error('No RequestRedrawContext found. Have you wrapped your commands into ReglRoot?')
})

export function useRequestRedraw() {
  return useContext(RequestRedrawContext)
}
