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
import {Card, Col, Container, Row} from "react-bootstrap";
import BasketItem from "../basketItem/basketItem";
import SubmitBasketData from "../submitBasketData/submitBasketData";


export default class Basket extends React.Component {
	constructor(props) {
		super(props);
	}

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
						<Card>
							<Card.Header className="text-center">Ваші замовлення</Card.Header>
							<BasketItem/>
						</Card>
						<SubmitBasketData/>
					</Col>
				</Row>
			</Container>
		);
	}
}
