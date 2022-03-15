import type { ThemedCssFunction, ThemedStyledInterface } from 'styled-components'
import baseStyled from 'styled-components'
import {
  useTheme as baseUseTheme,
  keyframes as kf,
} from 'styled-components'
import { css as baseCss } from 'styled-components'

// trick to get correct types from
// https://github.com/styled-components/styled-components/issues/1589#issuecomment-435613664
export type ScanHubTheme = typeof theme
export const styled = baseStyled as ThemedStyledInterface<ScanHubTheme>
export const keyframes = kf
export const useTheme = baseUseTheme as () => ScanHubTheme
export const css = baseCss as ThemedCssFunction<ScanHubTheme>

export const theme = Object.freeze({
  color: {
    primary: 'var(--color-primary)',
    background: 'var(--color-background)',
    foreground: 'var(--color-foreground)',
  },
} as const)
