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
import {Button, Table} from "react-bootstrap";

export default class BasketItem extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			array: null,
			error: null,
			isLoaded: false,
			maxQuantity: null
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
	updateQuantity(value) {
		return value
	}

	/*
	 * BasketItem.cell(colIdx:number, rowIdx:number, item:object): React.Component
	 *
	 * Filter method for cell in table
	 */
	cell(colIdx, rowIdx, item) {
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
		axios(process.env.REACT_APP_CONFIRM_ORDER, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		}).then((response) => {
			this.setState({array: []});
			toast.success(response.data)
		}).catch((error) => {
			const message = error.data;
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
		axios(process.env.REACT_APP_BASKET_DATA_URL, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		})
			// .then(res => res.json())
			.then(
				result => {
					this.setState({
						isLoaded: true,
						array: result.data[0].lines
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

	render() {
		const {error, isLoaded} = this.state;
		if (error) {
			return <div>Помилка: {error.message}</div>;
		} else if (!isLoaded) {
			return <div>Завантаження...</div>;
		} else if (this.state.array.length === undefined || this.state.array.length === 0) {
			return (
				<div>У вас не має замовлень в корзині</div>
			)
		} else {
			return (
				<Fragment>
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
						{this.state.array.map((items, rowIdx) => (
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
				</Fragment>
			)

		}
	}
}
