import React, {Component} from "react";
import Chart from "react-apexcharts";
import SideNav, {NavIcon, NavItem, NavText} from "@trendmicro/react-sidenav";
import '@trendmicro/react-sidenav/dist/react-sidenav.css';
import {BrowserRouter, Route, Redirect, Switch} from 'react-router-dom'


class Graph extends Component {
    constructor(props) {
        super(props);

        this.state = {
            options: {
                chart: {
                    shadow: {
                        enabled: true,
                        color: '#000',
                        top: 18,
                        left: 7,
                        blur: 10,
                        opacity: 1
                    },
                    toolbar: {
                        show: false
                    }
                },
                colors: ['#77B6EA', '#545454'],
                dataLabels: {
                    enabled: true,
                },
                stroke: {
                    curve: 'smooth'
                },
                title: {
                    text: 'Average High & Low Temperature',
                    align: 'left'
                },
                grid: {
                    borderColor: '#e7e7e7',
                    row: {
                        colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                        opacity: 0.5
                    },
                },
                markers: {

                    size: 6
                },
                xaxis: {
                    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                    title: {
                        text: 'Month'
                    }
                },
                yaxis: {
                    title: {
                        text: 'Temperature'
                    },
                    min: 5,
                    max: 40
                },
                legend: {
                    position: 'top',
                    horizontalAlign: 'right',
                    floating: true,
                    offsetY: -25,
                    offsetX: -5
                }
            },
            series: [
                {
                    name: "High - 2013",
                    data: [28, 29, 33, 36, 32, 32, 33]
                },
                {
                    name: "Low - 2013",
                    data: [12, 11, 14, 18, 17, 13, 13]
                }
            ],
        }
    }

    render() {
        return (
            <div className="app" style={{paddingLeft: '50px'}}>

                < BrowserRouter>
                    <Route render={({location, history}) => (
                        <React.Fragment>
                            <SideNav
                                onSelect={(selected) => {
                                    const to = '/' + selected;
                                    if (location.pathname !== to) {
                                        history.push(to);
                                    }
                                }}
                            >
                                <SideNav.Toggle/>
                                <SideNav.Nav defaultSelected="home">
                                    <NavItem eventKey="home">
                                        <NavIcon>
                                            <i className="fa fa-fw fa-home" style={{fontSize: '1.75em'}}/>
                                        </NavIcon>
                                        <NavText>
                                            Home
                                        </NavText>
                                    </NavItem>
                                    <NavItem eventKey="devices">
                                        <NavIcon>
                                            <i className="fa fa-fw fa-device" style={{fontSize: '1.75em'}}/>
                                        </NavIcon>
                                        <NavText>
                                            Devices
                                        </NavText>
                                    </NavItem>
                                </SideNav.Nav>
                            </SideNav>
                            <main>
                                <Route path="/" exact component={props => alert(0)}/>
                                <Route path="/home" component={props => alert(1)}/>
                                <Route path="/devices" component={props => alert(2)}/>
                            </main>
                        </React.Fragment>
                    )}
                    />
                </ BrowserRouter>
                <div className="row">
                    <div className="mixed-chart">
                        <Chart
                            options={this.state.options}
                            series={this.state.series}
                            type="line"
                            width="900"
                            height="700"
                        />
                    </div>
                </div>
                <style>{"\
                    .navbar{\
                      display:none;\
                    }\
                "}</style>
            </div>
        );
    }
}

export default Graph;