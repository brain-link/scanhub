import type { GLSL } from '../glsl'

/**
 * Function that produces GLSL code which modifies a vec2
 * of a given varname in-place.
 *
 * Example:
 * ```
 * varName => glsl`
 *    ${varname}.y += 0.5;
 * `
 * ```
 */
export type WrapFn = (varname: string) => GLSL
