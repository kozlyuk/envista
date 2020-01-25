/*
 *
 *   Navbar component.
 *
 *   @author           Andrey Perestyuk (Arrathilar)
 *   @email-primary    a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright        2020 ITEL-Service
 *
 *
 */

import React, {Fragment} from "react";
import {Link} from "react-router-dom";
import Auth from "../auth/auth";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";

class NavbarMenu extends React.Component {
	user = new Auth();

	render() {
		return (
			<Fragment>
				<div>
					<Navbar collapseOnSelect expand="lg" className="top-nav">
						<div className="container">
							<Navbar.Brand href="#home"><Link to="/" className="mr-auto m-0 brand w-nav-brand p-0">
								<img
									src={this.props.brandLogo}
									height={50}
									alt="brand"
									className="image-2"
								/>
							</Link></Navbar.Brand>
							<Navbar.Toggle aria-controls="responsive-navbar-nav"/>
							<Navbar.Collapse id="responsive-navbar-nav" className="menu-list">
								<Nav className="ml-auto">
									<Link style={{color: "#222222", padding: "20px"}} to="/">
										Головна
									</Link>
									<a
										href="https://envista.toriccalculator.com/(S(3p54nq0ludca5hrzdtsqdtfl))/UserAgreement.aspx"
										target="_blank"
										rel="noopener noreferrer"
										className=""
										style={{maxWidth: 940, color: "#222222", padding: "20px"}}>
										Калькулятор
									</a>
									{this.props.userIsStaff ? <Link
										style={{
											maxWidth: 940,
											color: "#222222",
											display: "inline-block",
											padding: "20px"
										}}
										to="/warehouse">
										Поповнення складу
									</Link> : ""}
									<Link
										style={{
											maxWidth: 940,
											color: "#222222",
											display: "inline-block",
											padding: "20px"
										}}
										to="/basket">
										Корзина
									</Link>
									<Link
										style={{
											maxWidth: 940,
											color: "#222222",
											display: "inline-block",
											padding: "20px"
										}}
										to="/logout"
										onClick={() => {
											this.user.logout();
										}}>
										Вийти ({this.props.userEmail})
									</Link>
								</Nav>
							</Navbar.Collapse>
						</div>
					</Navbar>
				</div>

			</Fragment>
		);
	}
}

export default NavbarMenu;
