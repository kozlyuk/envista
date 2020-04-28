/**
 * @author          Andrey Perestyuk (Arrathilar)
 * @email-primary   a.perestyuk@itel.rv.ua
 * @email-secondary arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright       2020 ITEL-Service
 *
 */

import React, {Fragment} from "react";
import {Col, Container, Row, Table} from "react-bootstrap";
import axios from "axios";
import Auth from "../auth/auth";
import OrderLine from "./orderLine/OrderLine";

export default class Cabinet extends React.Component {
  /**
   * Cabinet constructor
   *
   * @param props
   */
  constructor(props) {
    super(props);
    this.state = {
      data: null
    }
    this.user = new Auth();
  }

  componentDidMount() {
    axios(`${process.env.REACT_APP_GET_ORDERS_LIST}${this.props.userPk}/`, {
      headers: {
        "Authorization": "Token " + this.user.getAuthToken(),
      }
    }).then((response) => {
      this.setState({
        isLoaded: true,
        data: response.data
      })
    })
      .catch((error) => {
        console.warn(error.response.data)
      })
  }

  render() {
    const {isLoaded} = this.state;
    if (!isLoaded) {
      return <h3 className="text-center">Завантаження...</h3>;
    } else {
      return (
        <Container>
          <Fragment>
            <Row>
              <Col className="text-center">
                <h2 className="text-muted">Особистий кабінет</h2>
              </Col>
            </Row>
            <Row>
              <Col>
                <h4 className="text-center">Історія ваших замовлень</h4>
                <Table responsive bordered hover className="mb-0">
                  <thead>
                  <tr>
                    <th className="text-center">Номер замовлення</th>
                    <th className="text-center">Статус</th>
                    <th className="text-center">Дата замовлення</th>
                    <th className="text-center">Кількість лінз</th>
                    <th className="text-center">Вартість</th>
                  </tr>
                  </thead>
                  <tbody>
                  {this.state.data.map((orderLine) => (
                    <OrderLine data={orderLine}/>
                  ))}
                  </tbody>
                </Table>
              </Col>
            </Row>
          </Fragment>
        </Container>
      )
    }
  }
}