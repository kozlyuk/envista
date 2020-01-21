/*
 *
 *   Price component
 *
 *   @author                  Andrey Perestyuk (Arrathilar)
 *   @email-primary           a.perestyuk@itel.rv.ua
 *   @email-secondary         arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright               2020 ITEL-Service
 *
 *
 */

import React from "react";

export default class BasketPrice extends React.Component {
	constructor(props) {
		super(props);
	}

	calculcatePrice(colIdx, rowIdx) {
		const quantity = this.props.array[rowIdx].line[2];
		const pricePerUnit = this.props.array[rowIdx].line[3];
		return quantity * pricePerUnit;
	}

	render() {
		return (
			<td key={this.props.colIdx}>
				{this.calculcatePrice(this.props.colIdx, this.props.rowIdx)}
			</td>
		)
	}
}


