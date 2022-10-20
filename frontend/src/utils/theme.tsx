import * as React from 'react';
import colors from '@mui/joy/colors';
import { deepmerge } from '@mui/utils';
import { createTheme, experimental_extendTheme as extendMuiTheme } from '@mui/material/styles';

declare module '@mui/material/styles' {
    interface Theme {
        navigation: { height: string },
        patientView: { 
            toolbarHeight: string;
            drawerWidth: string;
            recordsWidth: string;
        },
    }

    // allow configuration using `createTheme`
    interface ThemeOptions {
        navigation?: { height?: string },
        patientView?: { 
            toolbarHeight?: string;
            drawerWidth?: string;
            recordsWidth?: string;
        },
    }
}

const muiTheme = extendMuiTheme({
    // This is required to point to `var(--joy-*)` because we are using `CssVarsProvider` from Joy UI.
    cssVarPrefix: 'joy',
    colorSchemes: {
        light: {
            palette: {
                primary: { 
                    main: colors.blue[500]
                },
                grey: colors.grey,
                error: { 
                    main: colors.red[500] 
                },
                info: { 
                    main: colors.purple[500] 
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

const customProps = createTheme(muiTheme, {
    navigation: {
        height: '64px',
    },
    patientView: {
        toolbarHeight: '54px',
        drawerWidth: '300px',
        recordsWidth: '300px',
    }
});

export default deepmerge(muiTheme, customProps);