//pages
import HomePage from './pages/HomePage'
import AuthPage from './pages/AuthPage'


// routes
import {HOME_PAGE, AUTH_PAGE} from './utils/consts'

export const authRoutes = [
    {
        path: HOME_PAGE,
        Component: HomePage
    },
]

export const publicRoutes = [
    {
        path: AUTH_PAGE,
        Component: AuthPage
    },
]