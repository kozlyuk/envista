/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React, {Fragment} from "react";
import axios from "axios";
import {toast} from "react-toastify";
import Auth from "../auth/auth";

export default class BasketInputNumber extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      array: this.props.orderArray,
      maxQuantity: this.props.orderArray[this.props.rowIdx][1].line[7]
    };
    this.user = new Auth();
    this.authToken = this.user.getAuthToken();
  }

  /*
   * BasketInputNumber.changeValue(rowIdx?, colIdx?, counter:number, target): void
   *
   * onChange handler send data to API.
   * When success - update state
   * When error - drop error in toast
   */
  changeValue(rowIdx, colIdx, counter, target) {
    Number.parseInt(rowIdx);
    Number.parseInt(colIdx);
    const itemPk = this.props.orderArray[this.props.rowIdx][1].line[6];
    const newQty = Number.parseInt(target.value);
    console.log(this.state.array)
    let newArray = [...this.state.array];
    newArray[rowIdx][1].line[4] = newQty;
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

  /*
   * BasketInputNumber.calculatePrice(colIdx:number, rowIdx:number): summaryPrice:number
   *
   * Get column adn row coordinate
   * return summary price from state
   */
  calculcatePrice(colIdx, rowIdx) {
    const quantity = this.props.orderArray[this.props.rowIdx][1].line[4];
    const pricePerUnit = this.props.orderArray[this.props.rowIdx][1].line[5];
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
                                           max={!this.props.preOrder && this.state.maxQuantity}
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