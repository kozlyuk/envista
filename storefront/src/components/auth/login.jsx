import React, {Component} from "react";
import {Container} from "react-bootstrap";
import Auth from "../auth/auth";
import "./auth.css";


export default class Login extends Component {
	constructor(props) {
		super(props);
		this.handleChange = this.handleChange.bind(this);
		this.handleSubmit = this.handleSubmit.bind(this);
		this.state = {
			email: null,
			password: null,
		}
	}

	handleChange(event) {
		// this.setState({value: event.target.value.toLowerCase()});
		//TODO: validations
	}

	/*
	 * Login.handleSubmit(event): void
	 * collect data from target form, and send to Auth.login method
	 */
	handleSubmit(event) {
		event.preventDefault();
		let user = new Auth();
		const target = event.target;
		const email = target.email.value;
		const password = target.password.value;
		this.setState({
			password: password,
			email: email
		});
		user.login(email, password).then(r => {
			return r;
		})
	}

	render() {
		return (
			<Container className="auth-container">
				<div className="box">
					<form onSubmit={this.handleSubmit}>
						<h1>Вхід</h1>
						<div className="group">
							<input name="email" className="inputMaterial" type="email" required/>
							<span className="highlight"/>
							<span className="bar"/>
							<label>Email</label>
						</div>
						<div className="group">
							<input name="password" className="inputMaterial" type="password" required/>
							<span className="highlight"/>
							<span className="bar"/>
							<label>Пароль</label>
						</div>
						<button id="buttonlogintoregister">Вхід</button>
					</form>
				</div>
			</Container>
		);
	}
}
