import React, {Component} from 'react';
import PropTypes from 'prop-types';
import cookie from "react-cookies";

class Modal extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.state = {
            username: null,
            email: null,
            errors: {}
        };
        console.log('and ii');
    }

    createPost(data) {
        const endpoint = '/signup/';
        const csrfToken = cookie.load('csrftoken');
        let thisComp = this;
        if (csrfToken !== undefined) {
            console.log('pooooooo');
            console.log(data);
            let lookupOptions = {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                data: JSON.stringify(data),
                body: JSON.stringify(data),
                credentials: 'include'
            };

            fetch(endpoint, lookupOptions)
                .then(function (response) {
                    window.location.reload();

                }).then(function (responseData) {
                console.log(responseData)

            }).catch(function (error) {
                console.log("error", error);
                alert("An error occured, please try again later.")
            })
        }
    }

    handleSubmit(event) {
        event.preventDefault();
        console.log(this.state)
        let data = this.state;

        console.log(data)
        this.createPost(data)
    }

    handleInputChange(event) {
        event.preventDefault();
        console.log(event.target.name, event.target.value);
        let key = event.target.name;
        let value = event.target.value;
        this.setState({
            [key]: value
        })
    }

    componentDidMount() {
        this.setState({
            username: null,
            email: null,
        })
    }

    render() {
        // Render nothing if the "show" prop is false
        if (!this.props.show) {
            return null;
        }

        // The gray background
        const backdropStyle = {
            top: 0,
            bottom: 0,
            left: 0,
            right: 0,
            backgroundColor: 'rgba(0,0,0,0.3)',
            padding: 50
        };

        // The modal "window"
        const modalStyle = {
            backgroundColor: '#fff',
            borderRadius: 5,
            maxWidth: 500,
            minHeight: 300,
            margin: '0 auto',
            padding: 30
        };

        return (
            <div className="backdrop" style={{backdropStyle}}>
                <div className="modal" style={{modalStyle}}>
                    {this.props.children}
                    <form onSubmit={this.handleSubmit}>
                        <div className='form-group'>
                            <label htmlFor='title'>Name</label>
                            <input type='text' id='title' name='username' className='form-control' placeholder='Name'
                                   onChange={this.handleInputChange}
                                   required='required'/>
                        </div>
                        <div className='form-group'>
                            <label htmlFor='content'>Email</label>
                            <input type='email' id='title' name='email' className='form-control' placeholder='Email'
                                   onChange={this.handleInputChange}
                                   required='required'/>

                        </div>
                        <div className='form-group'>
                            <label htmlFor='content'>Password</label>
                            <input type='password' id='title' name='password' className='form-control'
                                   onChange={this.handleInputChange}
                                   placeholder='Password'
                                   required='required'/>

                        </div>
                        <div className='form-group'>
                            <label htmlFor='content'>Confirm Password</label>
                            <input type='password' id='title' name='password2' className='form-control'
                                   placeholder='Password'
                                   onChange={this.handleInputChange}
                                   required='required'/>

                        </div>
                        <div className='form-group'>
                            <label htmlFor='draft'>
                                <input type='checkbox' id='draft' name='access' className='mr-2'
                                />
                                Access</label>
                        </div>
                        <button className='btn btn-primary'>Save</button>
                    </form>
                    <div className="footer">
                        <button onClick={this.props.onClose}>
                            Close
                        </button>
                        <button onClick={this.props.signIN}>
                            Sign In
                        </button>
                        <a className="btn btn-primary" href="/signin/login/facebook">Login with Facebook</a>
                        <a className="btn btn-primary" href="/signin/login/google-oauth2">Google</a>
                    </div>
                </div>
            </div>
        );
    }
}

Modal.propTypes = {
    onClose: PropTypes.func.isRequired,
    show: PropTypes.bool,
    children: PropTypes.node,
    signIN: PropTypes.node
};


export default Modal;