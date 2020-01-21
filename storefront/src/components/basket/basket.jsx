/*
 *
 *   Basket component.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React from "react";
import {Col, Container, Row} from "react-bootstrap";
import {createBrowserHistory} from "history";
import BasketItem from "../basketItem/basketItem";


export default class Basket extends React.Component {
	constructor(props) {
		super(props);
	}

	history = createBrowserHistory();

	render() {
		return (
			<Container>
				<Row>
					<Col className="text-center">
						<h2 className="text-muted">Корзина</h2>
					</Col>
				</Row>
				<Row>
					<Col>
						<h4 className="text-center">Ваші замовлення</h4>
						<BasketItem/>
					</Col>
				</Row>
			</Container>
		);
	}
}

