/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";

class Footer extends React.Component {
  render() {
    return (
      <div className="footer">
        <div className="container w-container">
          <p className="paragraph">
            {this.props.title}
          </p>
        </div>
      </div>
    );
  }
}

export default Footer;
