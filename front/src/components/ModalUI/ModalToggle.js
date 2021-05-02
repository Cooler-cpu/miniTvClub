import React from 'react'

//portal
import ModalPortal from '../../Portal/ModalPortal'

//UI
import ModalWindowUI from './ModalWindowUI'

import Button from 'react-bootstrap/Button'



class ModalToggle extends React.Component{
    constructor(props){
        super(props);
        this.state = {showModal: false};

        this.handleShow = this.handleShow.bind(this);
        this.handleHide = this.handleHide.bind(this);
    }

    handleShow(){
        this.setState({showModal: true});
    }

    handleHide(){
        this.setState({showModal:false});
    }

    render(){
        const modal = this.state.showModal ? (
            <ModalPortal>

                {/* <ModalWindowUIEditBalanse/> подключить верстку модального*/} 
                
                <ModalWindowUI handleHide={this.handleHide}/>

                {/* <Button onClick={this.handleHide} className="close-modal__button" variant="contained" color="primary">
                Закрыть
                </Button> */}

                {/* <Button onClick={this.handleHide} variant="primary">Закрыть</Button> */}

            </ModalPortal>
        ) : null;

        return (
            <div className="app">
        
                    <Button onClick={this.handleShow} variant="primary">{this.props.buttonOpenModalName}</Button>

                {modal}
                 
            </div>
        )
    }
}


export default ModalToggle