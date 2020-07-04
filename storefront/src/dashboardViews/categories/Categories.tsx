/*
 * @author     Andrey Perestyuk (Arrathilar)
 * @email       a.perestyuk@itel.rv.ua
 * @email       arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright  2020 ITEL-Service
 *
 */

import React, {Component} from 'react';
import Aux from "../../hoc/_Aux";
import {Button, Card, CardBody, CardColumns, CardText, CardTitle} from "reactstrap";
import catalogueMock from "../../__mocks__/catalogue";
import Loader from '../../App/layout/Loader'

interface CategoriesInterface {
  data: Category[] | null,
  isLoaded: boolean
}

type Category = {
  name: string,
  description: string
}

export default class Categories extends Component<any, CategoriesInterface> {

  state = {
    data: null,
    isLoaded: false
  }

  componentDidMount() {
    this.setState({
      data: catalogueMock,
      isLoaded: true,
    })
  }

  render() {
    const data: any = this.state.data;
    if (this.state.isLoaded) {
      return (
        <Aux>
          <CardColumns>
            {data?.map((item: Category) => (
              <Card>
                <CardBody>
                  <CardTitle>{item.name}</CardTitle>
                  {/*<CardSubtitle>Card subtitle</CardSubtitle>*/}
                  <CardText>{item.description}</CardText>
                  <Button size="sm" block color="info">Редагувати</Button>
                </CardBody>
              </Card>
            ))}
          </CardColumns>
        </Aux>
      )
    } else {
      return <Loader/>
    }
  }
}