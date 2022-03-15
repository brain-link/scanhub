export type OpenDialogProps<T extends string> = {
  title?: string
  message?: string
  body?: string | JSX.Element
  actions: {
    value: T
    autoFocus?: boolean
    text: string | JSX.Element
  }[]
  isModal?: boolean
  onEsc?: unknown
  onClickOutside?: unknown
} & (
    | {
      isModal: false
      onEsc?: never
      onClickOutside?: T
    }
    | {
      isModal: true
      onEsc?: T
      onClickOutside?: never
    }
  )

export type DialogSystemOpenFn = <T extends string>(props: OpenDialogProps<T>) => Promise<T>
