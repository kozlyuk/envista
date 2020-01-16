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

import React from "react";
import Auth from "../auth/auth";
import {Table} from "react-bootstrap";

export default class BasketItem extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			array: [],
			error: null,
			isLoaded: false
		};
		this.user = new Auth();
		this.authToken = this.user.getAuthToken();
	}

	cell(colIdx, item) {
		if (colIdx === 2) {
			return (<td key={colIdx}><input className="form-control"
											type="number"
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
		} else {
			return (<td key={colIdx}>{item}</td>)
		}
	}

	componentDidMount() {
		fetch(process.env.REACT_APP_BASKET_DATA_URL, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		})
			.then(res => res.json())
			.then(
				result => {
					this.setState({
						isLoaded: true,
						array: result[0].lines
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
		} else {
			return (
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
								this.cell(colIdx, item)
							))}
						</tr>
					))}
					</tbody>
				</Table>
			);
		}
	}
}
