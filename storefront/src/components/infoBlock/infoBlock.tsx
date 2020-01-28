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
import ReactHtmlParser from 'react-html-parser';

export default class InfoBlock extends React.Component<{ info: string, pdfUrl: string }> {
	render() {
		let info: string;
		({info} = this.props);
		return (
			<ListGroup className="ml-4 mr-4" variant="flush" defaultActiveKey="#link1">
				<ListGroup.Item className="text-center" action href={this.props.pdfUrl}>
					Перегляд PDF
				</ListGroup.Item>
				<ListGroup.Item className="text-center">Інформація</ListGroup.Item>
				<ListGroup.Item>
					{ReactHtmlParser(info)}
				</ListGroup.Item>
			</ListGroup>
		);
	}
}
