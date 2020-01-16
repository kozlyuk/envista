import React from "react";
import Wrapper from "./components/wrapper/wrapper";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";


export default class App extends React.Component {


	render() {
		return (
			<div className="App">
				<header className="main-container">
					<Wrapper/>
				</header>
			</div>
		)
	}

	;
}
