import { useCallback, useState } from 'react'
import { deferred } from 'utils'
import { Dialog } from './Dialog'
import { DialogSystemContext } from './DialogSystemContext'
import type { DialogSystemOpenFn, OpenDialogProps } from './types'

type DialogState<T extends string> = {
  /** Key generated by crypto.randomUUID() */
  key: string
  props: OpenDialogProps<T>
  resolve: (v: T) => void
}

export function DialogSystem({ children }: React.PropsWithChildren<{}>) {
  const [dialogs, setDialogs] = useState<DialogState<string>[]>([])

  const openDialog = useCallback<DialogSystemOpenFn>(
    function _<T extends string>(props: OpenDialogProps<T>) {
      const { promise, resolve } = deferred<T>()
      const state: DialogState<string> = {
        key: crypto.randomUUID(),
        props,
        resolve: action => {
          setDialogs(prev => prev.filter(d => d !== state))
          // @ts-expect-error typescript can't infer type correctly
          resolve(action)
        },
      }
      setDialogs(prev => [...prev, state])
      return promise
    },
    []
  )

  return (
    <DialogSystemContext.Provider value={openDialog}>
      {dialogs.map(({ key, resolve, props }) => (
        <Dialog key={key} resolve={resolve} {...props} />
      ))}
      {children}
    </DialogSystemContext.Provider>
  )
}
