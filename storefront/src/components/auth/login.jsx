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
			username: null,
			password: null,
		}
	}

	handleChange(event) {
		// this.setState({value: event.target.value.toLowerCase()});
		//TODO: validations
	}

	handleSubmit(event) {
		event.preventDefault();
		let user = new Auth();
		const target = event.target;
		const username = target.username.value;
		const password = target.password.value;
		this.setState({
			password: password,
			username: username
		});
		user.login(username, password)
	}

	static validation() {

	}

	render() {
		return (
			<Container>
				<div className="box">
					<form onSubmit={this.handleSubmit}>
						<h1>Вхід</h1>
						<div className="group">
							<input name="username" className="inputMaterial" type="text" required/>
							<span className="highlight"/>
							<span className="bar"/>
							<label>Username</label>
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
				;

				{/*<form onSubmit={this.handleSubmit}>*/}
				{/*	<h3>Sign In</h3>*/}

				{/*	<div className="form-group">*/}
				{/*		<label>Username</label>*/}
				{/*		<input name="username" onChange={this.handleChange} type="text" className="form-control"*/}
				{/*			   placeholder="Enter username"/>*/}
				{/*	</div>*/}

				{/*	<div className="form-group">*/}
				{/*		<label>Password</label>*/}
				{/*		<input name="password" type="password" className="form-control" placeholder="Enter password"/>*/}
				{/*	</div>*/}

				{/*	<div className="form-group">*/}
				{/*		<div className="custom-control custom-checkbox">*/}
				{/*			<input type="checkbox" className="custom-control-input" id="customCheck1"/>*/}
				{/*			<label className="custom-control-label" htmlFor="customCheck1">*/}
				{/*				Remember me*/}
				{/*			</label>*/}
				{/*		</div>*/}
				{/*	</div>*/}

				{/*	<button type="submit" className="btn btn-primary btn-block">*/}
				{/*		Submit*/}
				{/*	</button>*/}
				{/*	<p className="forgot-password text-right">*/}
				{/*		Forgot <a href="#">password?</a>*/}
				{/*	</p>*/}
				{/*</form>*/}
			</Container>
		);
	}
}
