import * as React from 'react';

// export default function PatientPage() {
//     return(
//         <div>Hello World!</div>
//     )
// }


// import { GlobalStyles } from '@mui/system';
import { CssVarsProvider, useColorScheme } from '@mui/joy/styles';
// import type { Theme } from '@mui/joy/styles';
import { styled } from '@mui/material/styles';
import AspectRatio from '@mui/joy/AspectRatio';
import Avatar from '@mui/joy/Avatar';
import AvatarGroup from '@mui/joy/AvatarGroup';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Card from '@mui/joy/Card';
import CardOverflow from '@mui/joy/CardOverflow';
import CardCover from '@mui/joy/CardCover';
import CardContent from '@mui/joy/CardContent';
import Typography from '@mui/joy/Typography';
import TextField from '@mui/joy/TextField';
import IconButton from '@mui/joy/IconButton';
import ListDivider from '@mui/joy/ListDivider';
import Sheet from '@mui/joy/Sheet';
import List from '@mui/joy/List';
import ListItem from '@mui/joy/ListItem';
import ListItemButton from '@mui/joy/ListItemButton';
import ListItemContent from '@mui/joy/ListItemContent';
import Drawer from '@mui/material/Drawer';
import Divider from '@mui/material/Divider';

// Icons import
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded';
import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded';
// import GridViewRoundedIcon from '@mui/icons-material/GridViewRounded';
import FindInPageRoundedIcon from '@mui/icons-material/FindInPageRounded';
import MenuIcon from '@mui/icons-material/Menu';
import FolderOpenIcon from '@mui/icons-material/FolderOpen';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import CloseIcon from '@mui/icons-material/Close';
import BookRoundedIcon from '@mui/icons-material/BookRounded';
import AddSharpIcon from '@mui/icons-material/AddSharp';

import Procedures from './ProcedureComponent';


const drawerWidth = 300;

const Main = styled('div', { shouldForwardProp: (prop) => prop !== 'open' }) <{ open?: boolean }>(
    ({ theme, open }) => (
        {
            flexGrow: 1,
            display: 'flex',
            flexDirection: 'column',
            minHeight: '100%',
            transition: theme.transitions.create('margin', {
                    easing: theme.transitions.easing.sharp,
                    duration: theme.transitions.duration.leavingScreen,
            }),
            marginLeft: 0,
            ...(open && {
                transition: theme.transitions.create('margin', {
                    easing: theme.transitions.easing.easeOut,
                    duration: theme.transitions.duration.enteringScreen,
                }),
                marginLeft: drawerWidth
            })
        }
    )
);

function ColorSchemeToggle() {
  const { mode, setMode } = useColorScheme();
  const [mounted, setMounted] = React.useState(true);
  React.useEffect(() => {
    setMounted(true);
  }, []);
  if (!mounted) {
    return <IconButton size="sm" variant="outlined" color="primary" />;
  }
  return (
    <IconButton
        id="toggle-mode"
        variant="outlined"
        color="primary"
        size="sm"
        onClick={() => {
            if (mode === 'light') {
                setMode('dark');
            } else {
                setMode('light');
            }
        }}
    >
      {mode === 'light' ? <DarkModeRoundedIcon /> : <LightModeRoundedIcon />}
    </IconButton>
  );
}

export default function FilesExample() {

  const [sidePanelOpen, setSidePanelOpen] = React.useState(true);

  return (
    // TODO: Find better solution for minHeigh property (fully expand div in vertical direction)
    <div id="page-container" style={{ width: '100%', position: 'relative', minHeight:'92vh' }}>
        <Drawer
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: drawerWidth,
                }
            }}
            PaperProps={{ style: { position: 'absolute' } }}
            BackdropProps={{ style: { position: 'absolute' } }}
            ModalProps={{
                container: document.getElementById('page-container'),
                style: { position: 'absolute' }
            }}
            variant="persistent"
            anchor="left"
            open={sidePanelOpen}
        >
            <Box sx={{ bgcolor: 'background.componentBg' }}>

                <Box>
                    <Typography level="h5" sx={{ p:2 }}>Patient Info</Typography>
                    <Divider />
                    <Typography sx={{ p:2 }}>Some patient information in a table view goes here...</Typography>
                </Box>

                <Divider />

                <Box>
                    <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                        <Typography level="h5">Procedures</Typography>
                        <IconButton size='sm' variant='outlined'>
                            <AddSharpIcon />
                        </IconButton>
                    </Box>
                    
                    <Divider />
                    <Procedures />
                </Box>

            </Box>
            

        </Drawer>

        <Main open={sidePanelOpen}>
            <Box sx={{ display: 'grid', gridTemplateRows: '54px auto', gridTemplateColumns: '1fr', bgcolor: 'background.componentBg'}}>
                
                {/* Toolbar */}
                <Box sx={{ 
                    p: 1.5,
                    display: 'flex', 
                    flexDirection: 'row', 
                    bgcolor: 'background.componentBg',
                    justifyContent: 'space-between',
                    alignItem: 'center', 
                    borderBottom: '1px solid',
                    borderColor: 'divider',
                    top: 0,
                    position: 'sticky',
                }}>
                    <IconButton
                        id="toggle-mode"
                        size="sm"
                        variant="outlined"
                        color="primary"
                        onClick={() => { setSidePanelOpen(!sidePanelOpen) }}
                    >
                        <MenuIcon />
                    </IconButton>
                    <ColorSchemeToggle />
                </Box>

                {/* Main Content */}
                <Box sx={{ display: 'flex', height: '100%' }}>

                    <Box sx={{ width: '300px', bgcolor: 'background.componentBg'}}> 

                        <Box sx={{ p: 2, display: 'flex', flexDirection:'row', justifyContent:'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                            <Typography level="h5">Records</Typography>
                            <IconButton size='sm' variant='outlined'>
                                <AddSharpIcon />
                            </IconButton>
                        </Box>

                        <Divider />

                        <Procedures />

                    </Box>
                    <Box sx={{ flexGrow: 1, bgcolor: '#eee' }}>
                        {/* <Procedures /> */}
                        <Typography sx={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}> View </Typography>
                    </Box>
                    
                </Box>

            </Box>
        </Main>
    </div>
  );
}
