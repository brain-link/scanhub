import { useEffect, useRef } from 'react'
import type { OpenDialogProps } from './types'

export type DialogProps<T extends string> = OpenDialogProps<T> & {
  resolve: (value: T) => void
}

export function Dialog({
  actions,
  body,
  isModal,
  message,
  onClickOutside,
  onEsc,
  resolve,
  title,
}: DialogProps<string>) {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const formRef = useRef<HTMLFormElement>(null)
  useEffect(
    () => {
      const dialog = dialogRef.current
      const form = formRef.current
      if (dialog === null || form === null) return

      /** User is able to close the dialog using ESC key (if modal) */
      const onCancel = (ev: Event) => {
        if (onEsc === undefined) {
          ev.preventDefault()
          return
        }
        resolve(onEsc)
      }

      /** User is able to close the dialog by clicking away (if not modal) */
      const onClick = () => {
        if (dialog.matches(':focus-within')) {
          return
        }
        if (onClickOutside !== undefined) {
          resolve(onClickOutside)
        }
      }

      /** Close happens when user chooses an action */
      const onClose = () => {
        resolve(dialog.returnValue)
      }

      window.addEventListener('click', onClick)
      dialog.addEventListener('cancel', onCancel)
      dialog.addEventListener('close', onClose)

      if (dialog.open) {
        console.warn(`Dialog was already open. This could be due to hot-reload.`)
      } else {
        if (isModal) {
          dialog.showModal()
        } else {
          dialog.show()
        }
      }

      const elemToAutofocus = dialog.querySelector('[data-autofocus]')
      if (elemToAutofocus instanceof HTMLElement) {
        elemToAutofocus.focus()
      }

      return () => {
        dialog.removeEventListener('close', onClose)
        dialog.removeEventListener('cancel', onCancel)
        window.removeEventListener('click', onClick)
      }
    },
    [isModal, onClickOutside, onEsc, resolve]
  )
  return (
    <dialog ref={dialogRef} tabIndex={-1}>
      <form ref={formRef} method='dialog'>
        {title !== undefined && <h3>{title}</h3>}
        {message !== undefined && <span>{message}</span>}
        {body}
        <menu>
          {actions.map(({ value, text, autoFocus }, i) => (
            <button
              key={i}
              value={value}
              data-autofocus={autoFocus}
            >{text}</button>
          ))}
        </menu>
      </form>
    </dialog>
  )
}
