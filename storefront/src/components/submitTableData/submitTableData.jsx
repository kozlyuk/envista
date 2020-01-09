import React from "react";
import { Button } from "react-bootstrap";

export default class Submit extends React.Component {
	constructor(props) {
		super(props);
	}

	send(purchase) {
		const url = "http://localhost:3004/data";
		console.log(this.props.purchaseList);
		fetch(url, {
			method: "post",
			headers: {
				"Content-type": "application/json; charset=UTF-8"
			},
			body: JSON.stringify(this.purchase)
		})
			.then(function(data) {
				console.log("Request succeeded with JSON response", data);
			})
			.catch(function(error) {
				console.log("Request failed", error);
			});
	}

	render() {
		return (
			<div className="text-center mb-4">
				<Button
					variant="outline-success"
					size="sm"
					onClick={() => {
						this.send(this.props.purchaseList);
					}}>
					Оформити замовлення
				</Button>
			</div>
		);
	}
}
