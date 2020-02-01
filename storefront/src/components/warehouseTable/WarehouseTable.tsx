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

import React, {Fragment} from "react";
import {Table} from "../table/table";
import Loader from "react-loader-spinner";
import ButtonBackground from "../buttonBackground/buttonBackground";
import {toast} from "react-toastify";
import axios from "axios";
import {Sticky, StickyContainer} from "react-sticky";
import "./style.css"

interface WarehouseTableProps {
	getData: any;
	reset: any;
}

export default class WarehouseTable extends Table implements WarehouseTableProps {

	constructor(props: any) {
		super(props);
		this.state = {
			rows: [],
			columnsName: [],
			error: null,
			isLoaded: false,
		};
	}

	/*
	 * increaseQty(counter?, columnIdx?, rowIdx?): void
	 *
	 * decrease counter of item quantities and write to state
	 */
	increaseQty(counter: number, columnIdx: number, rowIdx: number) {
		const newQty = counter >= 0 ? counter + 1 : 0;
		let newArray: any[];
		newArray = [...this.state.rows];
		newArray[rowIdx].quantities[columnIdx] = newQty;
		this.sendData(rowIdx, columnIdx)
			.then(() => {
					this.setState({rows: newArray}
					)
				}
			)
			.catch(error => {
				const message = error.response.data;
				toast.error(message);
			});
		return void 0;
	}


	getArray(columnsName: any, rows: any) {
		return void 0;
	}

	clickHandler() {
		const {REACT_APP_PURCHASE_DATA_RESET}: any = process.env;
		axios(REACT_APP_PURCHASE_DATA_RESET, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		}).then((result) => {
			this.forceUpdate();
			const {REACT_APP_WAREHOUSE_TABLE_DATA}: any = process.env;
			this.loadData(REACT_APP_WAREHOUSE_TABLE_DATA);
		})
			.catch((error) => {
				const message = error;
				console.log(message)
				// toast.error(message);
			})
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

	loadData(url: string) {
		axios(url, {
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
	}

	componentDidMount() {
		const {REACT_APP_WAREHOUSE_TABLE_DATA}: any = process.env;
		this.loadData(REACT_APP_WAREHOUSE_TABLE_DATA);
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
				<Fragment>
					<div className="row">
						<table className="table-bordered col mb-4 header-fixed">
							<StickyContainer>
								<colgroup>
									<col style={{width: 50, minWidth: 50}}/>
								</colgroup>
								<Sticky style={{zIndex: 1000}}>{({style}) =>
									<thead style={style} className="rc-table-thead sticky">
									<tr>
										<th style={{width: "57px"}} className="rc-table-row-cell-break-word"/>
										{this.state.columnsName.map((name: string, rowIdx: number) => (
											<th style={{width: "57px"}} key={rowIdx}
											    className="rc-table-row-cell-break-word text-center bg-light">
												{name}
											</th>
										))}
									</tr>
									</thead>
								}</Sticky>
								<tbody className="rc-table-tbody sticky">
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
							</StickyContainer>
						</table>
					</div>
					<div className="row">
						<button onClick={() => {
							this.clickHandler()
						}} className="btn btn-sm btn-outline-warning mb-3 ml-auto mr-auto">Очистити зміни
						</button>
					</div>
				</Fragment>
			);
		}
	}

	reset: any;
}