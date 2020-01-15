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
					‍Glistening-Free Hydrophobic AcrylicThe ideal combination of stable performance
					and predictabilityAberration-Free AsphericFenestrated, step-vaulted haptics with
					56° Contact angle and square posterior edge optic are designed to optimize 360°
					Capsular contact2360° posterior square edge with haptic-optic junction designed
					to minimise PCOPolished for a smooth optic surfaceUnique fenestrated,
					step-vaulted haptics with 56° contact angle are designed to maximise stability•
					91 % of patients had ≤ 5° rotation from day of surgery to 6 months1• 3° absolute
					mean rotation at 6 months1• 0.28 mm mean decentration1
				</ListGroup.Item>
			</ListGroup>
		);
	}
}
