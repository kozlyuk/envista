import React from "react";
import { Link } from "react-router-dom";

class Navbar extends React.Component {
	logOut() {
		fetch("http://localhost:3004/auth")
			.then(res => res.json())
			.then(
				result => {
					console.log(result);
				},
				error => {}
			);
	}
	render() {
		return (
			<div
				data-collapse="medium"
				data-animation="default"
				data-duration={400}
				className="navbar w-nav p-0 pl-4 pr-4">
				<div className="d-flex justify-content-between w-container-flex">
					<a href="#" className="mr-auto m-0 brand w-nav-brand p-0">
						<img
							src="https://uploads-ssl.webflow.com/5e01df57cdae92c47396eee8/5e048287478a40140bf39ce3_logo-crop.svg"
							height={50}
							alt="brand"
							className="image-2"
						/>
					</a>
					<nav role="navigation" className="w-nav-menu p-0">
						<a href="#" className="nav-link w-nav-link" style={{ maxWidth: 940 }}>
							<Link to="/">Vendor main page</Link>
						</a>
						<a
							href="https://envista.toriccalculator.com/(S(3p54nq0ludca5hrzdtsqdtfl))/UserAgreement.aspx"
							target="_blank"
							className="nav-link-2 w-nav-link"
							style={{ maxWidth: 940 }}>
							Calculator
						</a>
						<a className="nav-link-3 w-nav-link" style={{ maxWidth: 940 }}>
							<Link style={{ maxWidth: 940 }} to="/basket">
								Корзина
							</Link>
						</a>
						<a className="nav-link-3 w-nav-link" style={{ maxWidth: 940 }}>
							<Link
								style={{ maxWidth: 940 }}
								to="/logout"
								onClick={() => {
									this.logOut();
								}}>
								Logout
							</Link>
						</a>
					</nav>
					<div className="w-nav-button">
						<div className="w-icon-nav-menu" />
					</div>
				</div>
				<div className="w-nav-overlay" data-wf-ignore />
			</div>
		);
	}
}

export default Navbar;
