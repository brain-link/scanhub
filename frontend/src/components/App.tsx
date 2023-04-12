import * as React from 'react';
import { Outlet } from 'react-router-dom';

import Box from '@mui/joy/Box';
import CssBaseline from '@mui/joy/CssBaseline';
import { GlobalStyles } from '@mui/system';
import { CssVarsProvider } from '@mui/joy/styles';

import Navigation from './Navigation';
import theme from '../utils/theme';


export default function App() {
  return (
    <CssVarsProvider
      defaultMode="dark"
      disableTransitionOnChange
      theme={theme}
    >
      <CssBaseline />
      <GlobalStyles
        styles={{
          ':root': {
            '--Collapsed-breakpoint': '769px', // form will stretch when viewport is below `769px`
            '--Cover-width': '40vw', // must be `vw` only
            '--Form-maxWidth': '700px',
            '--Transition-duration': '0.4s', // set to `none` to disable transition
            // '--Navigation-height': '64px',  // set height of navigation bar
            // '--PatientView-toolbarHeight': '54px',
            // '--PatientView-drawerWidth': '300px',
            // '--PatientView-recordWidth': '300px',
          },
        }}
      />          
      <Navigation />

      {/* Main content */}
      <Box sx={{ 
          m: 0,
          p: 0,
          // pt: 8,
          gap: 2,
          justifyContent: 'start',
          display: 'flex',
          flexDirection: 'row',
          maxHeight: '100vh'
      }}>
          <Outlet />
      </Box>
    </CssVarsProvider>
  );
}
