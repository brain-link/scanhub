import * as React from 'react';
import { GlobalStyles } from '@mui/system';
import { Experimental_CssVarsProvider as CssVarsProvider, ThemeProvider } from '@mui/material/styles';
import { StyledEngineProvider } from '@mui/joy/styles';
import type { Theme } from '@mui/joy/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';


import ThemeCustomization from '../themes';
import theme from '../theme';
import { Navigation } from './Navigation';
import { Outlet } from 'react-router-dom';

export function App() {

  return (
    <ThemeCustomization>
        {/* <ThemeProvider theme={theme}> */}

        <CssBaseline /> 
        {/* <StyledEngineProvider injectFirst>
            <CssVarsProvider theme={theme}>

                <GlobalStyles<Theme>
                    styles={(theme) => ({
                    body: {
                        margin: 0,
                        fontFamily: theme.vars.fontFamily.body,
                    },
                    })}
                /> */}

        <Navigation />
        <Box sx={{ 
            // p: 2,
            m: 0,
            p: 0,
            pt: 10,
            gap: 2,
            justifyContent: 'start',
            display: 'flex', 
            flexDirection: 'row',
            // alignItems: 'center',
            width: 1,
            
        }}>
            <Outlet />
        </Box>
                
            {/* </CssVarsProvider>
        </StyledEngineProvider> */}

        {/* </ThemeProvider> */}
    </ThemeCustomization>
    
  );
}
