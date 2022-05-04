import { createContext, useContext } from 'react'
import type { CameraInstance, CameraTransform } from './types'

export const CameraContext = createContext<Pick<CameraInstance, 'glsl' | 'type'> | undefined>(undefined)
export function useCamera() {
  return useContext(CameraContext)
}

export const CameraTransformContext = createContext<CameraTransform | undefined>(undefined)
export function useCameraTransform() {
  return useContext(CameraTransformContext)
}
