import * as React from 'react';
// import CssBaseline from '@mui/material/CssBaseline';

import { StyledEngineProvider } from '@mui/joy/styles';
import Box from '@mui/material/Box';

// Theming
import type { Theme } from '@mui/joy/styles';
import { GlobalStyles } from '@mui/system';
import { deepmerge } from '@mui/utils';
import { experimental_extendTheme as extendMuiTheme } from '@mui/material/styles';
import colors from '@mui/joy/colors';
import {
  extendTheme as extendJoyTheme,
  CssVarsProvider,
  useColorScheme,
} from '@mui/joy/styles';


// Components
import { Navigation } from './Navigation';
import { Outlet } from 'react-router-dom';

const muiTheme = extendMuiTheme({
  // This is required to point to `var(--joy-*)` because we are using `CssVarsProvider` from Joy UI.
  cssVarPrefix: 'joy',
  colorSchemes: {
    light: {
      palette: {
        primary: {
          main: colors.blue[500],
        },
        grey: colors.grey,
        error: {
          main: colors.red[500],
        },
        info: {
          main: colors.purple[500],
        },
        success: {
          main: colors.green[500],
        },
        warning: {
          main: colors.yellow[200],
        },
        common: {
          white: '#FFF',
          black: '#09090D',
        },
        divider: colors.grey[200],
        text: {
          primary: colors.grey[800],
          secondary: colors.grey[600],
        },
      },
    },
    dark: {
      palette: {
        primary: {
          main: colors.blue[600],
        },
        grey: colors.grey,
        error: {
          main: colors.red[600],
        },
        info: {
          main: colors.purple[600],
        },
        success: {
          main: colors.green[600],
        },
        warning: {
          main: colors.yellow[300],
        },
        common: {
          white: '#FFF',
          black: '#09090D',
        },
        divider: colors.grey[800],
        text: {
          primary: colors.grey[100],
          secondary: colors.grey[300],
        },
      },
    },
  },
});

const joyTheme = extendJoyTheme();

// You can use your own `deepmerge` function.
// joyTheme will deeply merge to muiTheme.
const theme = deepmerge(muiTheme, joyTheme);

// const theme = deepmerge(extendJoyTheme(), extendMuiTheme());
// const theme = extendMuiTheme();

export function App() {

  return (
    <StyledEngineProvider injectFirst>
      <CssVarsProvider theme={theme}>
      {/* <CssVarsProvider> */}
        <GlobalStyles<Theme>
          styles={(theme) => ({
            body: {
              margin: 0,
              fontFamily: theme.vars.fontFamily.body,
            },
          })}
        />
        {/* <CssBaseline /> */}
        {/* <StyledEngineProvider injectFirst> */}

          <Navigation />

          {/* Main content */}
          <Box sx={{ 
              m: 0,
              p: 0,
              pt: 8,
              gap: 2,
              justifyContent: 'start',
              display: 'flex', 
              flexDirection: 'row',
              width: 1,
              
          }}>
              <Outlet />
          </Box>
        {/* </StyledEngineProvider> */}
      </CssVarsProvider>
    </StyledEngineProvider>
  );
}
