import React from "react";
import Wrapper from "./components/wrapper/wrapper";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Auth from "../src/components/auth/auth";
import Login from "../src/components/auth/login";


let user = new Auth();

export default function App() {
	return (
		<div className="App">
			<header className="main-container">
				{user.isAuthenticate() ? <Wrapper/> : <Login/>}
			</header>
		</div>
	);
}
