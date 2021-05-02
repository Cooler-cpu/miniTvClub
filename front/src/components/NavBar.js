import React from 'react'

//bootstrap
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import {Button, Container} from 'react-bootstrap'
import { connect } from 'react-redux';

import {useHistory} from 'react-router-dom'
import { NavLink } from 'react-router-dom';

const NavBar = (props) => {
   //const {isLoggedIn} = props;
   const isLoggedIn = true;

    console.log(isLoggedIn);

    return(
        <Navbar bg="dark" variant="dark">
        <Container>
            <NavLink to={'/'} style={{color: 'white'}}>
                miniTvClub
            </NavLink>
            {isLoggedIn ?
            <Nav className="ml-auto">

                {/* <Button variant="info">
                    Админ-панель
                </Button> */}

                 <Button variant="info">
                    Профиль
                </Button>

                <Button variant="info" 
                className="ml-2">
                
                     Выйти
                </Button>

            </Nav>
            :

            <Nav className="ml-auto" >
                <Button variant="info">Авторизация</Button>
            </Nav>
            }
        </Container>
    </Navbar>
    )
}

function mapStateToProps(state) {
    const { isLoggedIn } = state.auth;
    return {
      isLoggedIn,
    };
  }

export default connect(mapStateToProps)(NavBar)
// export default NavBar