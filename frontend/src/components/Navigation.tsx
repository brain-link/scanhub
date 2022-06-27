import { useState } from 'react'
import { Link, Outlet } from 'react-router-dom'
import { version } from '../utils/version'

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
    CButton,
    CFooter
} from '@coreui/react'


export function Navigation() {

    const [visible, setVisible] = useState(false)

    return (
        <>
        <CNavbar colorScheme="light" expand="lg" className="bg-light">

            <CContainer fluid className='ms-4 me-4 align-middle'>

                <CNavbarBrand href="https://www.brain-link.de/" className='me-5'>
                    <img
                        src="https://brain-link.de/wp-content/uploads/2022/03/ScanHub.svg"
                        // src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4'
                        alt=""
                        height="50"
                        className="d-inline-block align-top"
                    />
                </CNavbarBrand>

                {/* <CNavbarBrand className="me-5">
                    ScanHub
                </CNavbarBrand> */}

                <CNavbarToggler
                    aria-label="Toggle navigation"
                    aria-expanded={visible}
                    onClick={() => setVisible(!visible)}
                />

                <CCollapse className="navbar-collapse d-flex justify-content-between" visible={visible}>
                    <CNavbarNav>
                        <CNavItem>
                            <CNavLink to="/" active component={Link}>Dashboard</CNavLink>
                        </CNavItem>
                        <CNavItem>
                            <CNavLink to='/patients' component={Link}>Patients</CNavLink>
                        </CNavItem>
                        <CNavItem>
                            <CNavLink to='/devices' component={Link}>Devices</CNavLink>
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

        {/* <CFooter position='fixed' className='align-middle'>
        <div>
            <span><small>ScanHub &copy; 2022, Powered by BRAIN-LINK Medical Software Technologies</small></span>
            <CNavbarBrand href="https://www.brain-link.de/">
                <img
                    src='https://avatars.githubusercontent.com/u/27105562?s=200&v=4'
                    alt=""
                    height="30"
                    className="d-inline-block ms-2"
                />
            </CNavbarBrand>
        </div>
        </CFooter> */}

        </>
    )
}
