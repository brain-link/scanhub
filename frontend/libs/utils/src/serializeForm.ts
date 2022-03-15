export function serializeForm(form: HTMLFormElement) {
  return Object.fromEntries(new FormData(form).entries())
}
