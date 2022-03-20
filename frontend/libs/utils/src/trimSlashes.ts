export function trimSlashes(string: string) {
  // ^ beginning of string
  // \/+ one or more slashes
  // | or
  // \/+ one or more slashes
  // $ end of string
  // g all matches
  return string.replace(/^\/+|\/+$/g, '')
}
