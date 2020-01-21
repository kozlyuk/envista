/*
 *
 *   Navbar component.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React from "react";
import {Link} from "react-router-dom";
import Auth from "../auth/auth";

class Navbar extends React.Component {

	user = new Auth();

	render() {
		return (
			<div
				data-collapse="medium"
				data-animation="default"
				data-duration={400}
				className="navbar w-nav p-0 pl-4 pr-4">
				<div className="d-flex justify-content-between w-container-flex">
					<Link to="/" className="mr-auto m-0 brand w-nav-brand p-0">
						<img
							src={this.props.brandLogo}
							height={50}
							alt="brand"
							className="image-2"
						/>
					</Link>
					<nav role="navigation" className="w-nav-menu p-0">
						<Link style={{color: "#222222"}} to="/">Головна</Link>
						<a
							href="https://envista.toriccalculator.com/(S(3p54nq0ludca5hrzdtsqdtfl))/UserAgreement.aspx"
							target="_blank"
							rel="noopener noreferrer"
							className="nav-link-2 w-nav-link"
							style={{maxWidth: 940}}>
							Калькулятор
						</a>

						<Link
							style={{maxWidth: 940, color: "#222222", display: "inline-block", padding: "20px"}}
							to="/basket">
							Корзина
						</Link>

						<Link
							style={{maxWidth: 940, color: "#222222", display: "inline-block", padding: "20px"}}
							to="/logout"
							onClick={() => {
								this.user.logout();
							}}>
							Вийти ({this.props.userEmail})
						</Link>
					</nav>
					<div className="w-nav-button">
						<div className="w-icon-nav-menu"/>
					</div>
				</div>
				<div className="w-nav-overlay" data-wf-ignore/>
			</div>
		);
	}
}

export default Navbar;
