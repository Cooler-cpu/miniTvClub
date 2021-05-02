import React from 'react'
//import LoginComponent from '../components/AuthComponents/LoginComponent'

import LoginComponent from '../AuthComponents/LoginComponent'

import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import { Row } from 'react-bootstrap'

const ModalWindowUI = (props) => {
    return(
    <div className="modal">
        {/* <Container > */}
            <Row className="align-items-center modal-content"> 
            <LoginComponent handleHide={props.handleHide}/>
            {/* <Button onClick={props.handleHide} variant="primary">Закрыть</Button> */}
            </Row>
        {/* </Container> */}
    </div>
    )
}

// const ModalWindowUI = (props) => {
//     return(
//         <div className="overlay">
//             <div className="modal">
//                 <LoginComponent/>
//             </div>
//         </div>
//     )
// }

// const ModalWindowUI = (props) => {
//     return(
//          <div>
//             <div class="modal">
//                 <svg class="js-modal-close" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M23.954 21.03l-9.184-9.095 9.092-9.174-2.832-2.807-9.09 9.179-9.176-9.088-2.81 2.81 9.186 9.105-9.095 9.184 2.81 2.81 9.112-9.192 9.18 9.1z"/></svg>
//                 <div class="modal__content">
//                     <LoginComponent/>
//                 </div>
//                 </div>
//             <div class="overlay js-overlay-modal"></div>
//         </div>
//     )
// }

export default ModalWindowUI