/*
 *
 *   Main wrapper.
 *
 *   @author           Andrey Perestyuk (Arrathilar)
 *   @email-primary    a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright        2020 ITEL-Service
 *
 *
 */

import React, {Fragment} from "react";
import Navbar from "../navbar/navbar";
import Content from "../content/content";
import Footer from "../footer/footer";

import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import Basket from "../basket/basket";
import Login from "../auth/login";
import Auth from "../auth/auth";

import Loader from 'react-loader-spinner'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"
import axios from "axios";

class Welcome extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			isLoading: true,
			isAuthenticate: false
		};
		this.user = new Auth();
		this.getDataFromChild = this.getDataFromChild.bind(this)
	}

	/*
	 * Welcome.componentDidMount(): void
	 *
	 * Called immediately after a component is mounted.
	 * Setting state here will trigger re-rendering.
	 * Get user from API
	 * When success write in state isAuthenticate: true
	 * and user data
	 * When error write in state isAuthenticate: false
	 * and redirect to login page
	 */
	componentDidMount() {
		axios(process.env.REACT_APP_USER_DATA, {
			headers: {
				"Authorization": "Token " + this.user.getAuthToken(),
			}
		})
			.then(
				(response) => {
					if (response.status >= 400) {
						this.setState({
							isAuthenticate: false,
						})

					} else if (response.status < 400) {
						this.setState({
							isAuthenticate: true,
							user: response.data
						})
					}
				});
		setTimeout(() => {
			this.setState({
				isLoading: false
			})
		}, 1000)
	}

	/*
	 * Welcome.getDataFromChild(data?):void
	 * 
	 * method initiator for child component
	 * get from child props with brand logo and write to state
	 */
	getDataFromChild(data) {
		(this.setState({
			brandLogo: data
		}));
		return void 0
	}

	render() {
		if (this.state.isLoading) {
			return (
				<div className="loaderWrapper text-center mt-4">
					<Loader
						type="MutatingDots"
						color="#007bff"
						height={100}
						width={100}
						timeout={3000} //3 secs

					/>
					<h3 className="text-center text-muted">Завантаження...</h3>
				</div>);
		} else {
			return (
				<div>
					<Router>
						{this.state.isAuthenticate ? <Fragment>
								<Navbar brandLogo={this.state.brandLogo} userEmail={this.state.user.email}/>
								<div className="section">
									<div>
										<Switch>
											<Route path="/basket">
												<Basket/>
											</Route>
											<Route path="/">
												<Content getData={this.getDataFromChild}/>
											</Route>
										</Switch>
									</div>
								</div>
								<Footer/>
							</Fragment>
							: <Login/>}
					</Router>
				</div>)
		}
	}
}


export default Welcome;
