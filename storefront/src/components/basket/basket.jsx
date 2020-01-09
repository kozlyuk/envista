import React from "react";
import { Container, Row, Card, Col } from "react-bootstrap";
import BasketItem from "../basketItem/basketItem";

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
							<BasketItem />
						</Card>
					</Col>
				</Row>
			</Container>
		);
	}
}
