import React from "react";
import { Button } from "react-bootstrap";

export default class Submit extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="text-center mb-4">
				<Button
					variant="outline-success"
					size="sm"
					onClick={() => {
						console.log(this.props.purchaseList);
					}}>
					Оформити замовлення
				</Button>
			</div>
		);
	}
}
