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
import {FaTelegramPlane} from 'react-icons/fa';
import {MdInfoOutline, MdPictureAsPdf} from 'react-icons/md';

export default class InfoBlock extends React.Component<{ info: string, pdfUrl: string, telegram_bot_url: string }> {
	render() {
		let info: string;
		({info} = this.props);
		return (
			<ListGroup className="ml-4 mr-4" variant="flush" defaultActiveKey="#link1">
				<ListGroup.Item className="text-center" action href={this.props.pdfUrl}>
					<MdPictureAsPdf size="20"/> Перегляд PDF
				</ListGroup.Item>
				<ListGroup.Item className="text-center" action href={this.props.telegram_bot_url}>
					<FaTelegramPlane size="20"/> Телеграм бот
				</ListGroup.Item>
				<ListGroup.Item className="text-center"><MdInfoOutline size="20"/> Інформація</ListGroup.Item>
				<ListGroup.Item>
					{ReactHtmlParser(info)}
				</ListGroup.Item>
			</ListGroup>
		);
	}
}
