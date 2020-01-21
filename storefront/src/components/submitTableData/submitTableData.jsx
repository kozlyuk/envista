/*
 *
 *   Submit component for data from table.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React from "react";
import {Button} from "react-bootstrap";
import {withRouter} from 'react-router-dom'

class Submit extends React.Component {
	constructor(props) {
		super(props);
	}

	send(purchase) {
		const url = "http://localhost:3004/data";
		this.props.history.push('/basket')
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
					Перейти в корзину
				</Button>
			</div>
		);
	}
}

export default withRouter(Submit)
