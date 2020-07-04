/*
 * @author     Andrey Perestyuk (Arrathilar)
 * @email       a.perestyuk@itel.rv.ua
 * @email       arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright  2020 ITEL-Service
 *
 */

import React, {Component} from "react";
import {Card, Col, Row, Table} from "react-bootstrap";
import productMock from "../../__mocks__/products";
import Loader from '../../App/layout/Loader'

interface ProductListInterface {
  data: Product | null,
  isLoaded: boolean
}

type Product = {
  title: string,
  short_description: string,
  product_image: string,
  brand_name: string,
  brand_image: string,
  specifications_url: string,
  telegram_bot_url: string,
  footer: string
}

export default class ProductList extends Component<any, ProductListInterface> {
  public state = {
    data: null,
    isLoaded: false
  }

  public componentDidMount(): void {
    // @ts-ignore
    const productData: Product = productMock;
    this.setState({
      data: productData,
      isLoaded: true
    })
  }

  public render(): JSX.Element {
    const data: any = this.state.data
    if (this.state.isLoaded) {
      return (
        <Row>
          <Col>
            <Card>
              <Card.Header>
                <Card.Title as="h5">Список продуктів</Card.Title>
                {/*<span className="d-block m-t-5">use props <code>hover</code> with <code>Table</code> component</span>*/}
              </Card.Header>
              <Card.Body>
                <Table responsive hover>
                  <thead>
                  <tr>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Brand name</th>
                  </tr>
                  </thead>
                  <tbody>
                  {data.map((item: Product) => (
                    <tr>
                      <th scope="row">{item.title}</th>
                      <td>{item.short_description}</td>
                      <td>{item.brand_name}</td>
                    </tr>
                  ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      )
    } else {
      return (
        <Loader/>
      )
    }
  }
}