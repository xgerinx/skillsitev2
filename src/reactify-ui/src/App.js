import React, {Component} from 'react';
import {BrowserRouter, Route, Redirect, Switch} from 'react-router-dom'
import './App.css';
import Posts from './posts/Posts';
import Payment from "./payment/Payment";
import Graph from "./Admin/statistics";


class App extends Component {
    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route exact path='/payment/' component={Payment}/>
                    <Route exact path='/administrator/' component={Graph}/>
                    <Route exact path='/administrator/test/' component={Graph}/>
                    <Route component={Posts}/>
                </Switch>
            </BrowserRouter>
        );
    }
}

export default App;