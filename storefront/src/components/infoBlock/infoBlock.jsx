/*
 *
 *   Info block component.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React from "react";
import {ListGroup} from "react-bootstrap";

export default class InfoBlock extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<ListGroup className="ml-4 mr-4" variant="flush" defaultActiveKey="#link1">
				<ListGroup.Item className="text-center" action href="#link1">
					Перегляд PDF
				</ListGroup.Item>
				<ListGroup.Item className="text-center">Інформація</ListGroup.Item>
				<ListGroup.Item>
					‍{this.props.info}
				</ListGroup.Item>
			</ListGroup>
		);
	}
}
