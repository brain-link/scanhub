/**
 * Copyright (C) 2024, BRAIN-LINK UG (haftungsbeschränkt). All Rights Reserved.
 * SPDX-License-Identifier: GPL-3.0-only OR LicenseRef-ScanHub-Commercial
 *
 * Navigation.tsx is responsible for rendering the navigation bar at the top of the page.
 */
import AdminPanelSettingsSharpIcon from '@mui/icons-material/AdminPanelSettingsSharp'
import BuildSharpIcon from '@mui/icons-material/BuildSharp'
import DarkModeRoundedIcon from '@mui/icons-material/DarkModeRounded'
import LightModeRoundedIcon from '@mui/icons-material/LightModeRounded'
import LogoutSharpIcon from '@mui/icons-material/LogoutSharp'
import Person2SharpIcon from '@mui/icons-material/Person2Sharp'
import PersonSharpIcon from '@mui/icons-material/PersonSharp'
// Icons
// import HomeRoundedIcon from '@mui/icons-material/HomeRounded'
import RecentActorsSharpIcon from '@mui/icons-material/RecentActorsSharp'
import Avatar from '@mui/joy/Avatar'
import Box from '@mui/joy/Box'
import Button from '@mui/joy/Button'
import IconButton from '@mui/joy/IconButton'
import ListDivider from '@mui/joy/ListDivider'
import ListItemDecorator from '@mui/joy/ListItemDecorator'
import Dropdown from '@mui/joy/Dropdown'
import MenuButton from '@mui/joy/MenuButton'
import Menu from '@mui/joy/Menu'
import MenuItem from '@mui/joy/MenuItem'
import Typography from '@mui/joy/Typography'
import { useColorScheme } from '@mui/joy/styles'
import { useColorScheme as useMaterialColorScheme } from '@mui/material/styles'
import React, { useContext } from 'react'
import { useQueryClient } from 'react-query'
import { Link as RouterLink, useLocation } from 'react-router-dom'

import LoginContext from '../LoginContext'
// import { SettingsInputSvideoRounded } from '@mui/icons-material';
import { loginApi } from '../api'
import { UserRole } from '../generated-client/userlogin'
import ScanhubLogo from '../media/ScanhubLogo.png'
import NotificationContext from '../NotificationContext'


function ColorSchemeToggle() {
  const { mode, setMode } = useColorScheme()
  const { setMode: setMuiMode } = useMaterialColorScheme()
  const [mounted, setMounted] = React.useState(true)
  React.useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <IconButton size='sm' variant='outlined' color='primary' />
  }

  return (
    <IconButton
      id='toggle-mode'
      variant='outlined'
      color='primary'
      size='sm'
      onClick={() => {
        if (mode === 'light') {
          setMode('dark')
          setMuiMode('dark')
        } else {
          setMode('light')
          setMuiMode('light')
        }
      }}
    >
      {mode === 'light' ? <DarkModeRoundedIcon /> : <LightModeRoundedIcon />}
    </IconButton>
  )
}

export default function Navigation() {
  const loc = useLocation()
  const [user, setUser] = useContext(LoginContext)
  const [, setMessageObject] = useContext(NotificationContext)
  const queryClient = useQueryClient()

  // Menu elements
  const menuItems = [
    { id: 0, text: 'Patients', link: '/', icon: <RecentActorsSharpIcon /> },
    { id: 1, text: 'Templates', link: '/templates', icon: <BuildSharpIcon /> },
  ]
  if (user && user.role == UserRole.Admin) {
    menuItems.push({ id: 2, text: 'Users', link: '/users', icon: <Person2SharpIcon /> })
  }

  return (
    <Box
      component='header'
      className='Header'
      sx={{
        // height: navigation.height,
        height: 'var(--Navigation-height)',
        p: 2,
        gap: 2,
        bgcolor: 'background.surface',
        display: 'flex',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        gridColumn: '1 / -1',
        borderBottom: '1px solid',
        borderColor: 'divider',
        position: 'sticky',
        top: 0,
        zIndex: 'snackbar',
      }}
    >
      <IconButton variant='plain'>
        <a href='https://www.brain-link.de/' target='_blank' rel="noreferrer noopener">
          <img
            src={ScanhubLogo}
            alt=''
            height='40'
            className='d-inline-block'
          />
        </a>
      </IconButton>

      <Typography level='h4' sx={{ mr: 5 }}>
        ScanHub
      </Typography>

      <>
        {menuItems?.map((item) => (
          <Button
            component={RouterLink}
            to={item.link}
            size='sm'
            color='primary'
            startDecorator={item.icon}
            disabled={loc.pathname === item.link}
            variant={loc.pathname === item.link ? 'soft' : 'plain'}
            key={item.id}
            sx={{ display: 'inline-flex' }}
          >
            {item.text}
          </Button>
        ))}
      </>

      <Box sx={{ display: 'flex', flexDirection: 'row-reverse', width: '100%' }}>
        <ColorSchemeToggle />
      </Box>

      {/* User menu */}
      <Dropdown>
        <MenuButton
          slots={{root: IconButton}}
        >
          <Avatar variant='soft' color='primary' />
        </MenuButton>

        <Menu
          id='positioned-demo-menu'
          size='sm'
          onClose={() => {

          }}
          aria-labelledby='positioned-demo-button'
          placement='bottom-end'
          sx={{ zIndex: 'tooltip' }}
        >
          <MenuItem
            key='currentuser'
            disabled
            sx={{m: 'auto', fontWeight: 'bold'}}
          >
            {user?.username}
          </MenuItem>
          <ListDivider />
          <MenuItem
            key='profile'
            disabled
            onClick={() => {

            }}
          >
            <ListItemDecorator>
              <PersonSharpIcon />
            </ListItemDecorator>{' '}
            Profile
          </MenuItem>
          <MenuItem
            key='settings'
            disabled
            onClick={() => {

            }}
          >
            <ListItemDecorator>
              <AdminPanelSettingsSharpIcon />
            </ListItemDecorator>{' '}
            Settings
          </MenuItem>
          <ListDivider />
          <MenuItem
            key='logout'
            onClick={() => {
              loginApi
                .logoutApiV1UserloginLogoutPost({ headers: { Authorization: 'Bearer ' + user?.access_token } })
                .then(() => {
                  queryClient.invalidateQueries() // make sure the user who logs in next, can't see data not meant for them (e.g. list of all users)
                  setUser(null)
                })
                .catch((error) => {
                  setMessageObject({message: 'Error at logout: ' + error, type: 'warning'})
                })
            }}
          >
            <ListItemDecorator>
              <LogoutSharpIcon />
            </ListItemDecorator>{' '}
            Logout
          </MenuItem>
        </Menu>
      </Dropdown>
    </Box>
  )
}
