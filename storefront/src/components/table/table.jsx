/**
 * Table component.
 *
 * @author    Andrey Perestyuk (Arrathilar)
 * @email-primary a.perestyuk@itel.rv.ua
 * @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright 2020 ITEL-Service
 */


import React from "react";
import Auth from "../auth/auth";
import ButtonBackground from "../buttonBackground/buttonBackground";


export class Table extends React.PureComponent {
	constructor(props) {
		super(props);
		this.state = {
			rows: [],
			columnsName: [],
			error: null,
			isLoaded: false,
		};
		this.user = new Auth();
		this.authToken = this.user.getAuthToken();
	}


	/*
	 * decreaseQty(counter?, columnIdx?, rowIdx?): void
	 */

	// decrease counter of item quantities and write to state
	decreaseQty(counter, columnIdx, rowIdx) {
		const newQty = counter > 0 ? counter - 1 : 0;
		let newArray = [...this.state.rows];
		newArray[rowIdx].quantities[columnIdx] = newQty;
		this.sendData(rowIdx, columnIdx)
			.then(() => this.setState({rows: newArray}))
			.catch(error => alert(error.message)); // send get request to backend, then setstate with new quantity
		this.getData(counter, columnIdx, rowIdx);
	}

	/*
	 * Method sendData(rowIdx, columnIdx): Promise<void>
	 */

	async sendData(rowIdx, columnIdx) {
		const row = rowIdx + 1;
		const col = columnIdx + 1;
		await fetch(process.env.REACT_APP_ADD_TO_CARD + row + "/" + col, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		})
	}

	/*
	 * decreaseQty(counter, columnIdx, rowIdx): void
	 */

	// send data to parent component
	getData(counter, columnIdx, rowIdx) {
		if (counter !== 0) {
			this.props.getData((this.state.makePurchase = [columnIdx, rowIdx])); //maybe need to add id
		}
	}

	/*
	 * componentDidMount(): void
	 */

	//get data from backend => then mount component
	componentDidMount() {
		fetch(process.env.REACT_APP_TABLE_DATA, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		})
			.then(res => res.json())
			.then(
				result => {
					this.setState({
						isLoaded: true,
						rows: result[1].rows,
						columnsName: result[0].columns
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
		const {error, isLoaded} = this.state;
		if (error) {
			return <div>Помилка: {error.message}</div>;
		} else if (!isLoaded) {
			return <div>Загрузка...</div>;
		} else {
			return (
				<div className="row">
					<table className="table-bordered col mb-4">
						<colgroup>
							<col style={{width: 50, minWidth: 50}}/>
						</colgroup>
						<thead className="rc-table-thead text-center">
						<tr>
							<th className="rc-table-row-cell-break-word"/>
							{this.state.columnsName.map((name, rowIdx) => (
								<th key={rowIdx} className="rc-table-row-cell-break-word">
									{name}
								</th>
							))}
						</tr>
						</thead>
						<tbody className="rc-table-tbody">
						{this.state.rows.map((item, rowIdx) => (
							<tr key={rowIdx}
								className="rc-table-row rc-table-row-level-0"
								data-row-key={1}>
								<td className="rc-table-row-cell-break-word text-center">
									<span className="rc-table-row-indent indent-level-0"
										  style={{paddingLeft: 0}}>{item.row}</span>
								</td>
								{item.quantities.map((counter, columnIdx) => (
									<td
										key={columnIdx}
										className="rc-table-row-cell-break-word">
											<span
												className="rc-table-row-indent indent-level-0"
												style={{paddingLeft: 0}}
											/>
										<div>
											<ButtonBackground>
												<button
													style={{backgroundColor: "transparent"}}
													className="btn btn-sm btn-light btn-block"
													onClick={() =>
														this.decreaseQty(counter, columnIdx, rowIdx)
													}>
													{counter}
												</button>
											</ButtonBackground>
										</div>
									</td>
								))}
							</tr>
						))}
						</tbody>
					</table>
				</div>
			);
		}
	}
}