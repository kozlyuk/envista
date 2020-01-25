/*
 *
 *   Module_name.
 *
 *   @author                  Andrey Perestyuk (Arrathilar)
 *   @email-primary      a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright             2020 ITEL-Service
 *
 *
 */

import React from "react";
import {Table} from "../table/table";
import Loader from "react-loader-spinner";
import ButtonBackground from "../buttonBackground/buttonBackground";
import {toast} from "react-toastify";
import axios from "axios";

export default class WarehouseTable<WarehouseTable> extends Table {
	constructor(props: any) {
		super(Table);

		this.state = {
			rows: [],
			columnsName: [],
			error: null,
			isLoaded: false
		};
	}

	/*
	 * increaseQty(counter?, columnIdx?, rowIdx?): void
	 *
	 * decrease counter of item quantities and write to state
	 */
	increaseQty(counter: number, columnIdx: number, rowIdx: number) {
		const newQty = counter > 0 ? counter + 1 : 0;
		let newArray = [...this.state.rows];
		newArray[rowIdx].quantities[columnIdx] = newQty;
		this.sendData(rowIdx, columnIdx)
			.then(() => this.setState({rows: newArray}))
			.catch(error => {
				const message = error.response.data;
				toast.error(message);
			});
		// send get request to backend, then setstate with new quantity
		this.getData(counter, columnIdx, rowIdx);
		this.getArray(this.state.columnsName, this.state.rows);
		return void 0;
	}

	getData(counter: number, columnIdx: number, rowIdx: number): any {
		return
	}

	getArray(columnsName: any, rows: any): any {
		return;
	}

	async sendData(rowIdx: number, columnIdx: number): Promise<any> {
		const row = rowIdx + 1;
		const col = columnIdx + 1;
		const {REACT_APP_ADD_TO_PURCHASE}: any = process.env;
		return axios(REACT_APP_ADD_TO_PURCHASE + row + "/" + col + "/", {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		});
	}

	componentDidMount() {
		const {REACT_APP_WAREHOUSE_TABLE_DATA}: any = process.env;
		axios(REACT_APP_WAREHOUSE_TABLE_DATA, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		})
			.then(
				result => {
					this.setState({
						isLoaded: true,
						rows: result.data[1].rows,
						columnsName: result.data[0].columns
					});
				},
				error => {
					this.setState({
						isLoaded: true,
						error
					});
				}
			);
		return void 0;
	}

	public render() {
		const {error, isLoaded} = this.state;
		if (error) {
			return <div>Помилка: {error.message}</div>;
		} else if (!isLoaded) {
			return (
				<div className="loaderWrapper text-center mt-4">
					<Loader
						type="MutatingDots"
						color="#007bff"
						height={100}
						width={100}
						timeout={3000} //3 secs

					/>
					<h3 className="text-center text-muted">Завантаження...</h3>
				</div>)
				;
		} else {
			return (
				<div className="row">
					<table className="table-bordered col mb-4 header-fixed">
						<colgroup>
							<col style={{width: 50, minWidth: 50}}/>
						</colgroup>
						<thead style={{position: "sticky"}} className="rc-table-thead text-center">
						<tr>
							<th className="rc-table-row-cell-break-word"/>
							{this.state.columnsName.map((name: string, rowIdx: number) => (
								<th key={rowIdx} className="rc-table-row-cell-break-word">
									{name}
								</th>
							))}
						</tr>
						</thead>
						<tbody className="rc-table-tbody">
						{this.state.rows.map((item: { row: React.ReactNode; quantities: any[]; }, rowIdx: string | number | undefined) => (
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
														this.increaseQty(counter, columnIdx, rowIdx as number)
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