import { useMemo } from 'react'
import { Link, Outlet, useLocation } from 'react-router-dom'
import type { OpenDialogProps } from 'scanhub-ui'
import { Clock, useDialog } from 'scanhub-ui'
import { trimSlashes } from 'utils'
import { version } from '../version'

const logoutDialog: OpenDialogProps<'cancel' | 'logout'> = {
  title: 'Are you sure you want to log out?',
  actions: [
    { value: 'cancel', text: 'Cancel', autoFocus: true },
    { value: 'logout', text: 'Log out' },
  ],
  isModal: true,
  onEsc: 'cancel',
}

export function Navigation() {
  const { pathname } = useLocation()
  const openDialog = useDialog()
  const links = useMemo(
    () => {
      const pieces = trimSlashes(pathname).split('/')
      let to = ''
      return pieces.map((part, i) => {
        to += `/${part}`
        return <li key={i}><Link to={to}>{part}</Link></li>
      })
    },
    [pathname])
  return (
    <>
      <nav>
        <a href='#/' className='logo'>
          <img src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4' />
        </a>
        <ul className='breadcrumbs'>
          {links}
        </ul>
        <div className='grow' />
        <Link to='/patients'>Patients</Link>
        <Link to='/devices'>Devices</Link>
        <Link to='/docs'>Docs v{version}</Link>
        <Clock />
        <button onClick={async () => console.log(await openDialog(logoutDialog))}>Logout</button>
      </nav>
      <main>
        <Outlet />
      </main>
    </>
  )
}
