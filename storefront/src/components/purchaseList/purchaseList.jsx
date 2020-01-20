/*
 *
 *   Purchase list component.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React from "react";


export default class PurchaseList extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			rows: [],
			columns: []
		};
	}


	render() {
		if (this.props.purchaseList.length !== 0) {
			return (
				<div className="text-center mb-4 ml-4 mr-4">
					<h4>Обрано:</h4>
					<table className="table-bordered col mb-4">
						<tbody className="rc-table-tbody">
						<tr className="rc-table-row rc-table-row-level-0" data-row-key={1}>
							<td className="rc-table-row-cell-break-word text-center">
									<span
										className="rc-table-row-indent indent-level-0"
										style={{paddingLeft: 0}}>
										#
									</span>
							</td>
							<td className="rc-table-row-cell-break-word text-center">
									<span
										className="rc-table-row-indent indent-level-0"
										style={{paddingLeft: 0}}>
										Cylinder
									</span>
							</td>
							<td className="rc-table-row-cell-break-word text-center">
									<span
										className="rc-table-row-indent indent-level-0"
										style={{paddingLeft: 0}}>
										Diopter
									</span>
							</td>
						</tr>
						{this.props.purchaseList.map((item, index) => (
							<tr
								key={index}
								className="rc-table-row rc-table-row-level-0"
								data-row-key={1}>
								<td className="rc-table-row-cell-break-word text-center">
										<span
											className="rc-table-row-indent indent-level-0"
											style={{paddingLeft: 0}}>
											{index + 1}
										</span>
								</td>
								<td className="rc-table-row-cell-break-word text-center">
										<span
											className="rc-table-row-indent indent-level-0"
											style={{paddingLeft: 0}}>
											{this.props.array[0][1][item[1]].row} {/*[item[1]]*/}
										</span>
								</td>
								<td className="rc-table-row-cell-break-word text-center">
										<span
											className="rc-table-row-indent indent-level-0"
											style={{paddingLeft: 0}}>
											{this.props.array[0][0][item[0]]}
										</span>
								</td>
							</tr>
						))}
						</tbody>
					</table>
				</div>
			);
		} else {
			return (
				<div className="text-center mb-4">
					<h4>Оберіть товар натиснувши на комірку таблиці</h4>
				</div>
			);
		}
	}
}
