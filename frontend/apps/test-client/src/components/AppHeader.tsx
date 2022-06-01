import { useState } from 'react'
import { Link, Outlet } from 'react-router-dom'
import { version } from '../version'

import {
    CNavbarBrand,
    CContainer,
    CNavbar,
    CCollapse,
    CNavbarNav,
    CNavItem,
    CNavLink,
    CNavbarToggler,
    CForm,
    CButton
} from '@coreui/react'


// const logoutDialog: OpenDialogProps<'cancel' | 'logout'> = {
//     title: 'Are you sure you want to log out?',
//     actions: [
//       { value: 'cancel', text: 'Cancel', autoFocus: true },
//       { value: 'logout', text: 'Log out' },
//     ],
//     isModal: true,
//     onEsc: 'cancel',
//   }
  

export function Navigation() {

    const [visible, setVisible] = useState(false)

    // const openDialog = useDialog()

    return (
        <>
        <CNavbar colorScheme="light" expand="lg" className="bg-light">

            <CContainer fluid className='ms-4 me-4 align-middle'>

                <CNavbarBrand href="https://www.brain-link.de/">
                    <img
                        src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4'
                        alt=""
                        height="50"
                        className="d-inline-block align-top"
                    />
                </CNavbarBrand>

                <CNavbarBrand className="me-5">
                    ScanHub
                </CNavbarBrand>

                <CNavbarToggler
                    aria-label="Toggle navigation"
                    aria-expanded={visible}
                    onClick={() => setVisible(!visible)}
                />

                <CCollapse className="navbar-collapse d-flex justify-content-between" visible={visible}>
                    <CNavbarNav>
                        <CNavItem>
                            <CNavLink href="#" active>Dashboard</CNavLink>
                        </CNavItem>
                        <CNavItem>
                            <CNavLink to='/patients' component={Link}>Patients</CNavLink>
                        </CNavItem>
                        <CNavItem>
                            <CNavLink href="#">Devices</CNavLink>
                        </CNavItem>
                    </CNavbarNav>

                    <CNavbarNav>
                        <CNavItem>
                            <CNavLink href="#" disabled>V{version}</CNavLink>
                        </CNavItem>
                        <CForm className="container-fluid justify-content-start">
                            <CButton type="button" color="dark" variant="outline" className="me-2">
                                Logout
                            </CButton>
                        </CForm>
                    </CNavbarNav>

                </CCollapse>
            </CContainer>
        </CNavbar>

        <main>
            <Outlet />
        </main>
        </>

    )
}
