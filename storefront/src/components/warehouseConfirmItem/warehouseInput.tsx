/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React, {Fragment} from "react"
import Auth from "../auth/auth";
import axios from "axios";
import {toast} from "react-toastify";

interface WarehouseInputState {
  array?: any
}

interface WarehouseInputProps {
  title?: string
  requestUrl?: string
  sendUrl?: string
  array?: any
  updateQuantity?: any
}

export default class WarehouseInput extends React.Component<WarehouseInputProps, WarehouseInputState> {
  private user: Auth;
  private authToken: string | boolean;

  constructor(props: Readonly<WarehouseInputProps>) {
    super(props);
    this.state = {
      array: this.props.array,
    };
    this.user = new Auth();
    this.authToken = this.user.getAuthToken()
  }

  /*
   * WarehouseConfirmInputNumber.changeValue(rowIdx?, colIdx?, counter:number, target): void
   *
   * onChange handler send data to API.
   * When success - update state
   * When error - drop error in toast
   */
  changeValue(rowIdx: any, colIdx: any, counter: number, target: any) {
    Number.parseInt(rowIdx);
    Number.parseInt(colIdx);
    const itemPk = this.state.array[rowIdx].line[4];
    const newQty = Number.parseInt(target.value);
    let newArray = [...this.state.array];
    newArray[rowIdx].line[2] = newQty;
    const requestUrl = `${process.env.REACT_APP_CHANGE_PURCHASE_QUANTITY}${itemPk}/${newQty}/`;
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

  render() {
    return (
      <Fragment>
        <div>Warehouse input</div>
      </Fragment>
    )
  }
}