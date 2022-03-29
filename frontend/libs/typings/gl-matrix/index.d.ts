declare module 'gl-matrix' {
  export namespace vec2 {
    export function set<T extends vec2>(out: T, x: number, y: number): T;
  }
  export namespace vec4 {
    export function set<T extends vec4>(out: T, x: number, y: number, z: number, w: number): T;
    export function transformMat4<T extends vec4>(out: T, a: ReadonlyVec4, m: ReadonlyMat4): T;
    export function clone<T extends ReadonlyVec4>(a: T): T;
  }
}
