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
import {Table} from "react-bootstrap";

export default class BasketItem extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			array: [],
			error: null,
			isLoaded: false
		};
	}

	componentDidMount() {
		fetch(process.env.REACT_APP_BASKET_DATA_URL)
			.then(res => res.json())
			.then(
				result => {
					this.setState({
						isLoaded: true,
						array: result
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
						<th>Cylinder</th>
						<th>Diopter</th>
						<th>Кількість</th>
						<th>Вартість</th>
					</tr>
					</thead>
					<tbody>
					{this.state.array.map((items, rowIdx) => (
						<tr key={rowIdx}>
							<td>{rowIdx + 1}</td>
							{items.map((item, colIdx) => (
								<td key={colIdx}>{item}</td>
							))}
						</tr>
					))}
					</tbody>
				</Table>
			);
		}
	}
}
