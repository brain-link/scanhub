import { deepmerge } from '@mui/utils';
import { extendTheme as extendJoyTheme} from '@mui/joy/styles';
import { experimental_extendTheme as extendMuiTheme } from '@mui/material/styles'

declare module '@mui/joy/styles' {
  interface PaletteBackground {
    appBody: string;
    componentBg: string;
  }
}

const joyTheme = extendJoyTheme({
  cssVarPrefix: 'mui',
  colorSchemes: {
    light: {
      palette: {
        background: {
          appBody: 'var(--joy-palette-neutral-50)',
          componentBg: 'var(--joy-palette-common-white)',
        },
      },
    },
    dark: {
      palette: {
        background: {
          appBody: 'var(--joy-palette-common-black)',
          componentBg: 'var(--joy-palette-neutral-900)',
        },
      },
    },
  },
  fontFamily: {
    // display: "'Inter', var(--joy-fontFamily-fallback)",s
    // body: "'Inter', var(--joy-fontFamily-fallback)",
  },
});

const muiTheme = extendMuiTheme();

export default deepmerge(joyTheme, muiTheme);
