export function deferred<T>() {
  let resolve: (v: T) => void
  const promise = new Promise<T>(_resolve => {
    resolve = _resolve
  })
  return {
    // @ts-expect-error Typescript doesn't know this will be defined
    resolve,
    promise,
  }
}
