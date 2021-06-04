import React from 'react'

import tvImg from '../assets/img/tvImg.png'

import ModalToggle from '../components/ModalUI/ModalToggle'

const AuthContainer = () => {
    return(
        <div className="auth-container">


            <div className="row">
                <h1>Присоединяйтесь<br/> к miniTvClub прямо сейчас</h1>
            </div>
        {/* <div></div> */}
        {/* <img width={300} height={300} src={tvImg} alt="tvImg" /> */}

            <div className="col modal-auth_menu" style={auth_menuStyle} >
            {/* <img width={400} height={250} src={tvImg} alt="tvImg" /> */}
                <div className="col-sm modal-auth_menuBtn auth_menuBtn1">
                    <ModalToggle buttonOpenModalName="Авторизация"/>
                </div>

                <div className=" col-sm modal-auth_menuBtn auth_menuBtn2">
                    <ModalToggle buttonOpenModalName="Регистрация"/>
                </div>
            </div>

        </div>
    )
}

var auth_menuStyle={
    // backgroundImage: 'url(${tvImg})',
    backgroundImage: `url(${tvImg})`,
    height: '270px',
    width: '400px',
    backgroundPosition: 'center',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat'
}

const AuthPage = () => {
    return (
        <div className="container mt-3">

            <AuthContainer/>
        </div>
    )
}


export default AuthPage