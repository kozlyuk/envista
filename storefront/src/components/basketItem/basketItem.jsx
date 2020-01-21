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
import {Button, Table} from "react-bootstrap";
import axios from "axios";
import {toast} from "react-toastify";

export default class BasketItem extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			array: null,
			error: null,
			isLoaded: false
		};
		this.cell = this.cell.bind(this);
		this.user = new Auth();
		this.authToken = this.user.getAuthToken();
	}

	changeValue(rowIdx, colIdx, counter, target) {
		Number.parseInt(rowIdx);
		Number.parseInt(colIdx);
		const itemPk = this.state.array[rowIdx].line[4]
		const newQty = Number.parseInt(target.value);
		let newArray = [...this.state.array];
		newArray[rowIdx].line[2] = newQty;
		const requestUrl = `${process.env.REACT_APP_CHANGE_QUANTITY}${itemPk}/${newQty}`;
		axios(requestUrl, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		}).then((result) => {
			console.log(result)
			this.setState({
				array: newArray
			});
		})
			.catch((error) => {
				const message = error.response.data;
				toast.error(message);
			})
	}

	calculcatePrice(colIdx, rowIdx) {
		const quantity = this.state.array[rowIdx].line[2];
		const pricePerUnit = this.state.array[rowIdx].line[3];
		return quantity * pricePerUnit;
	}

	cell(colIdx, rowIdx, item) {
		if (colIdx === 2) {
			return (<td key={colIdx}><input className="form-control"
											type="number"
											onChange={(event) => {
												this.changeValue(rowIdx, colIdx, item, event.target)
											}}
											defaultValue={item}
											style={{
												height: 30,
												fontSize: 14,
												width: 100,
												marginLeft: "auto",
												marginRight: "auto",
												display: "flex",
												position: "relative",
											}}
			/>
			</td>)
		} else if (colIdx === 3) {
			return (<td key={colIdx}>
				{this.calculcatePrice(colIdx, rowIdx)}
			</td>)
		} else if (colIdx === 4) {
			return void 0
		} else {
			return (<td key={colIdx}>{item}</td>)
		}
	}

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
					<Table striped bordered hover className="mb-0">
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
