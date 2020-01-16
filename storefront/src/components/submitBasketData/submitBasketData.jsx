/*
 *
 *   Component for submit data from basket.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React, {Fragment} from "react";
import {Button} from "react-bootstrap";
import Auth from "../auth/auth";


export default class SubmitBasketData extends React.Component {
	constructor(props) {
		super(props);
		this.user = new Auth()
		this.authToken = this.user.getAuthToken()

	}


	handleClick() {
		fetch(process.env.REACT_APP_CONFIRM_ORDER, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		}).then(() => console.log("click"))
	}

	render() {
		return (
			<Fragment>
				<div className="text-center mt-4">
					<Button
						variant="outline-success"
						size="sm"
						onClick={() => {
							this.handleClick();
						}}>
						Підтвердити замовлення
					</Button>
				</div>
			</Fragment>
		)
	}
}