import React from 'react';
import {Switch, Route, Redirect} from 'react-router-dom'


import { authRoutes } from '../routes';
import { publicRoutes } from '../routes'

import {AUTH_PAGE} from '../utils/consts'


//redux 
import { connect } from "react-redux";

const AppRouter = (props) => { 
   // const {user} = false; 
   const { isLoggedIn } = props; //  redux

    let isAuth = false;

    console.log(isLoggedIn);

    return(
        <Switch>
            {/* {user.isAuth === true && authRoutes.map(({path, Component}) =>  */}
            {isLoggedIn === true && authRoutes.map(({path, Component}) => 
                <Route key={path} path={path} component={Component} exact/>
            )}
            {publicRoutes.map(({path, Component}) => 
                <Route key={path} path={path} component={Component} exact/>
            )}
            <Redirect to={AUTH_PAGE}/>  {/*перенаправление на страницу регистрации/авторизации еслии пользователь !auth */}
        </Switch>
    )
}

function mapStateToProps(state){
    const { isLoggedIn } = state.auth;
    return {
        isLoggedIn,
    }
}


export default connect(mapStateToProps)(AppRouter)