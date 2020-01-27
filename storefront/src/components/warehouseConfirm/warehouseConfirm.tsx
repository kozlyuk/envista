/*
 *
 *   Warehouse confirm component.
 *
 *   @author           1Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React from "react";
import {Container} from "react-bootstrap";
import {createBrowserHistory} from "history";
import WarehouseConfirmItem from "../warehouseConfirmItem/warehouseConfirmItem";


export default class WarehouseConfirm extends React.Component {

	/*
	 * browser history object
	 */
	history = createBrowserHistory();

	render() {
		return (
			<Container>

				<WarehouseConfirmItem/>

			</Container>
		);
	}
}
