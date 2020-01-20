/*
 *
 *   Main wrapper.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
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

class Welcome extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			isLoading: true,
			isAuthenticate: false
		};
		this.user = new Auth();
	}

	componentDidMount() {
		fetch(process.env.REACT_APP_USER_DATA, {
			headers: {
				"Authorization": "Token " + this.user.getAuthToken(),
				"WWW-Authenticate": "Token " + this.user.getAuthToken()
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
						})
					}
				});
		setTimeout(() => {
			this.setState({
				isLoading: false
			})
		}, 1000)
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
								<Navbar/>
								<div className="section">
									<div>
										<Switch>
											<Route path="/basket">
												<Basket/>
											</Route>
											<Route path="/">
												<Content/>
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
