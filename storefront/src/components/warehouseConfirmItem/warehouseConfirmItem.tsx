/*
 *
 *   Warehouse confirm item component.
 *
 *   @author                  Andrey Perestyuk (Arrathilar)
 *   @email-primary           a.perestyuk@itel.rv.ua
 *   @email-secondary         arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright               2020 ITEL-Service
 *
 *
 */

import React, {Fragment} from "react";
import {Button, Col, Row, Table} from "react-bootstrap";
import Auth from "../auth/auth";
import WarehouseInputNumber from "../warehouseInputNumber/warehouseInputNumber";
import axios from "axios";
import {toast} from "react-toastify";

/*
 * State interface
 */
interface WarehouseItemState {
	array?: any
	error?: any
	isLoaded?: boolean
	maxQuantity?: number
	isWarehouseActive?: boolean
}

export default class WarehouseConfirmItem extends React.Component<{}, WarehouseItemState> {
	private user: Auth;
	private authToken: any;

	constructor(props: any, state: any) {
		super(props, state);
		this.state = {
			array: null,
			error: null,
			isLoaded: false,
			maxQuantity: 0,
			isWarehouseActive: true
		};
		this.cell = this.cell.bind(this);
		this.user = new Auth();
		this.authToken = this.user.getAuthToken();
	}

	/*
     * WarehouseConfirmItem.updateQuantity(value)
     *
     * Middleware reducer.
     * Need to catch value from child component, and put to parent state
     * return same data as input
     */
	updateQuantity(value: number) {
		return value
	}

	/*
     * WarehouseConfirmItem.cell(colIdx:number, rowIdx:number, item:object): React.Component
     *
     * Filter method for cell in table
     s*/
	cell(colIdx: number, rowIdx: number, item: any) {
		if (colIdx === 4) {
			return (<WarehouseInputNumber colIdx={colIdx} rowIdx={rowIdx} item={item} array={this.state.array}
			                              updateQuantity={this.updateQuantity}/>)
		} else if (colIdx === 5 || colIdx === 6) {
			return void 0
		} else {
			return (<td key={colIdx}>{item}</td>)
		}
	}

	/*
     * WarehouseConfirmItem.handleClick(): void
     *
     * Method handler
     * When success - confirm order and put response to state
     * When error - drop error toast
     */
	handleClick() {
		const {REACT_APP_CONFIRM_PURCHASE}: any = process.env;
		axios(REACT_APP_CONFIRM_PURCHASE, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		}).then((response: any) => {
			this.setState({
				array: [],
				isWarehouseActive: false
			});
			// toast.success(response.data)
		}).catch((error: any) => {
			const message: any = error.data;
			toast.error(message);
		})
	}

	/*
	 * WarehouseConfirmItem.componentDidMount()
	 * Called immediately after a component is mounted. Setting state here will trigger re-rendering.
	 * Get data from API
	 * While error - drop error
	 */
	componentDidMount() {
		const {REACT_APP_PURCHASE_DATA_URL}: any = process.env;
		axios(REACT_APP_PURCHASE_DATA_URL, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		})
			// .then(res => res.json())
			.then(
				(result: any) => {
					this.setState({
						isLoaded: true,
						array: result.data[0].lines
					});
				},
				(error: any) => {
					this.setState({
						isLoaded: true,
						error
					});
				}
			);
		return void 0;
	}

	render() {
		const {error, isLoaded}: any = this.state;
		if (error) {
			return <h3 className="text-center">Помилка: {error.message}</h3>;
		} else if (!isLoaded) {
			return <h3 className="text-center">Завантаження...</h3>;
		} else if (!this.state.isWarehouseActive) {
			return (
				<div className="mt-4">
					<div className="checkmark-circle ml-auto mr-auto">
						<div className="background"></div>
						<div className="checkmark draw"></div>
					</div>
					<h3 className="text-success text-center">Зміни внесено!</h3>
				</div>
			)
		} else {
			return (
				<Fragment>
					<Row>
						<Col className="text-center">
							<h2 className="text-muted">Склад</h2>
						</Col>
					</Row>
					<Row>
						<Col>
							<h4 className="text-center">Підтвердіть внесення змін до складу</h4>
							<Table responsive striped bordered hover className="mb-0">
								<thead>
								<tr>
									<th>#</th>
									<th>Назва</th>
									<th>Сфера</th>
									<th>Циліндр</th>
									<th className="text-center">Кількість</th>
								</tr>
								</thead>
								<tbody>
								{this.state.array.map((items: { line: any[]; }, rowIdx: number) => (
									<tr key={rowIdx}>
										{items.line.map((item, colIdx) => (
											this.cell(colIdx, rowIdx, item)
										))}
									</tr>
								))}
								</tbody>
							</Table>
							<div className="text-center mt-4">
								<Button
									variant="outline-success"
									size="sm"
									onClick={() => {
										this.handleClick();
									}}>
									Підтвердити
								</Button>
							</div>
						</Col>
					</Row>
				</Fragment>)
		}
	}
}
