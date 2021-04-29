import React from 'react';
import {Switch, Route, Redirect} from 'react-router-dom'


import { authRoutes } from '../routes';
import { publicRoutes } from '../routes'


const DevicePage = () => {
   // const {user} = false; redux 

    let isAuth = false;

    console.log(isAuth);

    return(
        <Switch>
            {/* {user.isAuth === true && authRoutes.map(({path, Component}) =>  */}
            {isAuth === true && authRoutes.map(({path, Component}) => 
                <Route key={path} path={path} component={Component} exact/>
            )}
            {publicRoutes.map(({path, Component}) => 
                <Route key={path} path={path} component={Component} exact/>
            )}
            {/* <Redirect to={AUTH_ROUTE}/> */}
        </Switch>
    )
}

export default DevicePage;