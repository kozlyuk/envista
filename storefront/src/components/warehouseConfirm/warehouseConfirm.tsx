/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";
import {Container} from "react-bootstrap";
import {createBrowserHistory} from "history";
import WarehouseConfirmItem from "../warehouseConfirmItem/warehouseConfirmItem";


export default class WarehouseConfirm extends React.Component {

  /*
   * browser history object
   */
  history = createBrowserHistory();

  render() {
    return (
      <Container>

        <WarehouseConfirmItem/>

      </Container>
    );
  }
}

