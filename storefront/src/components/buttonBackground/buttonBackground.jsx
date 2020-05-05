/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";

export default class ButtonBackground extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isChecked: false
    }
  }

  doChecked(event) {
    this.setState({isChecked: true})
    console.log(this.props.orderStatus)
    if (this.props.orderStatus === 'order') {
      event.target.style.backgroundColor = "#159ba7"
    } else if (this.props.orderStatus === 'preOrder') {
      event.target.style.backgroundColor = "blue"
    }
    // this.props.orderStatus === "order" ? "#159ba7" : "black"
  }

  render() {
    return (
      <div style={{
        borderRadius: "5px",
        backgroundColor: "#ffff"
      }}
           onClick={(event) => {
             this.doChecked(event)
           }}>
        {this.props.children}
      </div>
    )
  }
}


