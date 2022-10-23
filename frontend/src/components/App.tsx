import * as React from 'react';
import { Outlet } from 'react-router-dom';

// Theming
import { GlobalStyles } from '@mui/system';
import { deepmerge } from '@mui/utils';
// import CssBaseline from '@mui/joy/CssBaseline';
import {
  extendTheme as extendJoyTheme,
  StyledEngineProvider,
  CssVarsProvider,
  Theme
} from '@mui/joy/styles';

import Box from '@mui/material/Box';

// Components
import Navigation from './Navigation';
import muiTheme from '../utils/theme';

// MUI joy theme will deeply merge to muiTheme
const joyTheme = extendJoyTheme();
const theme = deepmerge(muiTheme, joyTheme);

export default function App() {

  return (
    <StyledEngineProvider injectFirst>
      <CssVarsProvider theme={theme}>
        {/* <CssBaseline /> */}
        <GlobalStyles<Theme>
          styles={(theme) => ({
            body: {
              margin: 0,
              fontFamily: theme.vars.fontFamily.body,
            },
          })}
        />

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
              maxHeight: '100vh'
          }}>
              <Outlet />
          </Box>
        {/* </StyledEngineProvider> */}
      </CssVarsProvider>
    </StyledEngineProvider>
  );
}
