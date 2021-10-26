import React, {Component} from 'react';
import PropTypes from 'prop-types';
import cookie from "react-cookies";

class Payment extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
        this.state = {
            check_no: 1,
            country: null,
            username: null,
            email: null,
            errors: {},
            items: [
                {"name": "country", "type": "text"},
            ],
            credentials: 'include'
        };
    }

    createPost(data) {
        const endpoint = '/order/';
        const csrfToken = cookie.load('csrftoken');
        let thisComp = this;
        if (csrfToken !== undefined) {
            console.log(data);
            let lookupOptions = {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            };

            fetch(endpoint, lookupOptions)
                .then(res => res.json())
                .then(data => {
                    console.log(data);
                    window.location.href = "https://money.yandex.ru/api-pages/v2/payment-confirm/epl?orderId="+
                        data.check_no + "";

                }).catch(function (error) {
                console.log("error", error);
                alert("An error occured, please try again later.")
            })
        }
    }

    handleSubmit(event) {
        event.preventDefault();
        let data = this.state;
        this.createPost(data)
    }

    handleInputChange(event) {
        event.preventDefault();

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

        return (
            <div>
                {this.props.children}
                <form onSubmit={this.handleSubmit} style={{height: 500}}>
                    {this.state.items.map(item => (
                        <div className='form-group'>
                            <label htmlFor='title'>{item.name}</label>
                            <input type={item.type} id={item.name} name={item.name} className='form-control'
                                   placeholder={item.name}
                                   onChange={this.handleInputChange}
                                   required='required'/>
                        </div>
                    ))}
                    <button className='btn btn-primary'>Pay</button>
                </form>
            </div>
        );
    }
}


export default Payment;