/*
 *
 *   Input component for basket.
 *
 *   @author                  Andrey Perestyuk (Arrathilar)
 *   @email-primary      	  a.perestyuk@itel.rv.ua
 *   @email-secondary  		  arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 *   @copyright               2020 ITEL-Service
 *
 *
 */

import React, {Fragment} from "react";
import axios from "axios";
import {toast} from "react-toastify";
import Auth from "../auth/auth";

export default class BasketInputNumber extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			array: this.props.array,
			maxQuantity: this.props.array[this.props.rowIdx].line[5]
		};
		this.user = new Auth();
		this.authToken = this.user.getAuthToken();
	}

	changeValue(rowIdx, colIdx, counter, target) {
		Number.parseInt(rowIdx);
		Number.parseInt(colIdx);
		const itemPk = this.state.array[rowIdx].line[4];
		const newQty = Number.parseInt(target.value);
		let newArray = [...this.state.array];
		newArray[rowIdx].line[2] = newQty;
		const requestUrl = `${process.env.REACT_APP_CHANGE_QUANTITY}${itemPk}/${newQty}/`;
		axios(requestUrl, {
			headers: {
				"Authorization": "Token " + this.authToken
			}
		}).then((result) => {
			this.setState({
				array: newArray
			});
			this.props.updateQuantity(newArray);
		})
			.catch((error) => {
				const message = error.response.data;
				toast.error(message);
			})
	}

	calculcatePrice(colIdx, rowIdx) {
		const quantity = this.props.array[rowIdx].line[2];
		const pricePerUnit = this.props.array[rowIdx].line[3];
		return quantity * pricePerUnit;
	}

	render() {
		return (
			<Fragment>
				<td key={this.props.colIdx}><input className="form-control"
												   type="number"
												   onChange={(event) => {
													   this.changeValue(this.props.rowIdx, this.props.colIdx, this.props.item, event.target)
												   }}
												   defaultValue={this.props.item}
												   min="0"
												   max={this.state.maxQuantity}
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
				</td>
				<td key={this.props.colIdx}>
					{this.calculcatePrice(this.props.colIdx, this.props.rowIdx)} грн.
				</td>
			</Fragment>
		)
	}
}