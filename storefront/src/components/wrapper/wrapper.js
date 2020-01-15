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

import React from "react";
import Navbar from "../navbar/navbar";
import Content from "../content/content";
import Footer from "../footer/footer";

import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import Basket from "../basket/basket";

class Welcome extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div>
				<Router>
					<Navbar/>
					<div className="section">
						<div>
							<Switch>
								<Route path="/logout">
									<h1>LoginPage</h1>
								</Route>
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
				</Router>
			</div>
		);
	}
}

export default Welcome;
