/*
 *
 *   Basket item component.
 *
 *   @author    Andrey Perestyuk (Arrathilar)
 *   @email-primary a.perestyuk@itel.rv.ua
 *   @email-secondary  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright 2020 ITEL-Service
 *
 *
 */

import React, {Fragment} from "react";
import Auth from "../auth/auth";
import BasketInputNumber from "../basketInputNumber/basketInputNumber";
import axios from "axios";
import {toast} from "react-toastify";
import {Button, Col, Row, Table} from "react-bootstrap";
import "../basketItem/style.css"

interface State {
	array: any
	error: any
	isLoaded: boolean
	maxQuantity: number
	isBasketActive: boolean
}

export default class BasketItem extends React.Component<{}, State> {
	private user: Auth;
	private authToken: any;

	constructor(props: any, state: any) {
		super(props, state);
		this.state = {
			array: null,
			error: null,
			isLoaded: false,
			maxQuantity: 0,
			isBasketActive: true
		};
		this.cell = this.cell.bind(this);
		this.user = new Auth();
		this.authToken = this.user.getAuthToken();
	}

	/*
	 * BasketItem.updateQuantity(value)
	 *
	 * Middleware reducer.
	 * Need to catch value from child component, and put to parent state
	 * return same data as input
	 */
	updateQuantity(value: number) {
		return value
	}

	/*
	 * BasketItem.cell(colIdx:number, rowIdx:number, item:object): React.Component
	 *
	 * Filter method for cell in table
	 */
	cell(colIdx: number, rowIdx: number, item: any) {
		if (colIdx === 2) {
			return (<BasketInputNumber colIdx={colIdx} rowIdx={rowIdx} item={item} array={this.state.array}
			                           updateQuantity={this.updateQuantity}/>)
		} else if (colIdx === 3) {
			return void 0
		} else if (colIdx === 4 || colIdx === 5) {
			return void 0
		} else {
			return (<td key={colIdx}>{item}</td>)
		}
	}

	/*
	 * BasketItem.handleClick(): void
	 *
	 * Method handler
	 * When success - confirm order and put response to state
	 * When error - drop error toast
	 */
	handleClick() {
		const {REACT_APP_CONFIRM_ORDER}: any = process.env;
		axios(REACT_APP_CONFIRM_ORDER, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		}).then((response: any) => {
			this.setState({
				array: [],
				isBasketActive: false
			});
			// toast.success(response.data)
		}).catch((error: any) => {
			const message: any = error.data;
			toast.error(message);
		})
	}

	/*
	 * BasketItem.componentDidMount()
	 * Called immediately after a component is mounted. Setting state here will trigger re-rendering.
	 * Get data from API
	 * While error - drop error
	 */
	componentDidMount() {
		const {REACT_APP_BASKET_DATA_URL}: any = process.env;
		axios(REACT_APP_BASKET_DATA_URL, {
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
		} else if (!this.state.isBasketActive) {
			return (
				<div className="mt-4">
					<div className="checkmark-circle ml-auto mr-auto">
						<div className="background"></div>
						<div className="checkmark draw"></div>
					</div>
					<h3 className="text-success text-center">Дякуємо за покупку!</h3>
				</div>
			)
		} else if (this.state.array.length === undefined || this.state.array.length === 0) {
			return (
				<h3 className="text-center">У вас не має замовлень в корзині</h3>
			)
		} else {
			return (
				<Fragment>
					<Row>
						<Col className="text-center">
							<h2 className="text-muted">Корзина</h2>
						</Col>
					</Row>
					<Row>
						<Col>
							<h4 className="text-center">Ваші замовлення</h4>
							<Table responsive striped bordered hover className="mb-0">
								<thead>
								<tr>
									<th>#</th>
									<th>Назва</th>
									<th className="text-center">Кількість</th>
									<th>Вартість</th>
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
									Підтвердити замовлення
								</Button>
							</div>
						</Col>
					</Row>
				</Fragment>
			)

		}
	}
}
