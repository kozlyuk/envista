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
import Auth from "../auth/auth";


export default class PurchaseList extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			rows: [],
			columns: []
		};
	}

	//get data from backend => then mount component
	componentDidMount() {
		const user = new Auth();
		const authToken = user.getAuthToken();
		fetch(process.env.REACT_APP_PURCHASE_DATA_URL, {
			headers: {
				"Authorization": "Token " + authToken
			}
		})
			.then(res => res.json())
			.then(
				result => {
					const rowName = result[1].rows.map(item => {
						return item.row;
					});
					this.setState({
						isLoaded: true,
						rows: rowName,
						columns: result[0].columns
					});
				},
				error => {
					this.setState({
						isLoaded: true,
						error
					});
				}
			);
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
											{this.state.rows[item[1]]}
										</span>
								</td>
								<td className="rc-table-row-cell-break-word text-center">
										<span
											className="rc-table-row-indent indent-level-0"
											style={{paddingLeft: 0}}>
											{this.state.columns[item[0]]}
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
