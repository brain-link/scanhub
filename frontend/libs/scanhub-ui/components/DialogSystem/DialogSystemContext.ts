import { createContext, useContext } from 'react'
import type { DialogSystemOpenFn } from './types'

export const DialogSystemContext = createContext<DialogSystemOpenFn>(
  props => {
    console.error(props)
    throw new Error('No DialogSystemContext present, please wrap the app in <DialogSystem></DialogSystem>.')
  }
)

export function useDialog() {
  return useContext(DialogSystemContext)
}
