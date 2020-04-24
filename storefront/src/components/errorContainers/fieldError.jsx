/*
 * @author          Andrey Perestyuk (Arrathilar)
 * @email-primary   a.perestyuk@itel.rv.ua
 * @email-secondary arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright       2020 ITEL-Service
 *
 */

import React from "react";

export default class FieldError extends React.Component {

  render() {
    return (
      <small style={{position: "absolute"}} className="text-danger">
        {this.props.error}
      </small>
    );
  }

}