/*
 * @author     Andrey Perestyuk (Arrathilar)
 * @email       a.perestyuk@itel.rv.ua
 * @email       arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright  2020 ITEL-Service
 *
 */

import React, {Component} from 'react';
import Aux from "../../hoc/_Aux";
import {Card, Col, Row, Table} from "react-bootstrap";

export default class Categories extends Component<any, any> {
  render() {
    return (
      <Aux>
        <Row>
          <Col>
            <Card>
              <Card.Header>
                <Card.Title as="h5">Список категорій</Card.Title>
                {/*<span className="d-block m-t-5">use props <code>hover</code> with <code>Table</code> component</span>*/}
              </Card.Header>
              <Card.Body>
                <Table responsive hover>
                  <thead>
                  <tr>
                    <th>#</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Username</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr>
                    <th scope="row">1</th>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                  </tr>
                  <tr>
                    <th scope="row">2</th>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                  </tr>
                  <tr>
                    <th scope="row">3</th>
                    <td>Larry</td>
                    <td>the Bird</td>
                    <td>@twitter</td>
                  </tr>
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Aux>
    )
  }
}