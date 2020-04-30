/**
 * @author    Andrey Perestyuk (Arrathilar)
 * @email     a.perestyuk@itel.rv.ua
 * @email     arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright 2020 ITEL-Service
 *
 */

import React from "react";

export default class TableButton extends React.Component {

  /**
   * Table button constructor.
   *
   * @param props
   */
  constructor(props) {
    super(props);
    this.state = {
      orderStatus: null
    }
  }

  /**
   * Counter when do pre order.
   *
   * @type {number}
   * @private
   */
  _preOrderTriggerStatus = 0

  /**
   * Change button color.
   *
   * @param counter
   */
  changeButtonColor(counter) {
    if (counter === this._preOrderTriggerStatus) {
      this.setState({
        orderStatus: 'preOrder'
      })
    } else {
      this.setState({
        orderStatus: 'order'
      })
    }
  }

  getStatus() {
    return this.state.orderStatus
  }

  decreaseWrapper = (event) => {
    this.props.decreaseQty(event, this.props.counter, this.props.columnIdx, this.props.rowIdx);
    this.changeButtonColor(this.props.counter);
  }

  buttonStyle() {
    switch (this.state.orderStatus) {
      case "order":
        return "#159ba7"
      case "preOrder":
        return "#25ad35"
      default:
        return "#fff"
    }
  }

  render() {
    return (
      <div style={{
        borderRadius: "5px",
        backgroundColor: this.buttonStyle()
      }}>
        <button
          style={{backgroundColor: "transparent"}}
          className="btn btn-sm btn-light btn-block"
          onClick={this.decreaseWrapper}>
          {this.props.counter}
        </button>
      </div>
    )
  }
}