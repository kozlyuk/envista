/*
 * @author     Andrey Perestyuk (Arrathilar)
 * @email       a.perestyuk@itel.rv.ua
 * @email       arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright  2020 ITEL-Service
 *
 */

import React, {Component} from 'react';
import Aux from "../../hoc/_Aux";
import {Card, CardBody, CardColumns, CardImg, CardText, CardTitle} from "reactstrap";
import catalogueMock from "../../__mocks__/catalogue";
import Loader from '../../App/layout/Loader'
import {Link} from "react-router-dom";

interface CategoriesInterface {
  data: Category[] | null,
  isLoaded: boolean
}

type Category = {
  pk: number,
  name: string,
  description: string,
  image: string
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
                <Link to={`/categories/${item.pk}/edit`}>
                  <CardImg top width="100%" src={item.image} alt="Card image cap"/>
                  <CardBody>
                    <CardTitle className="text-secondary">{item.name}</CardTitle>
                    <CardText className="text-secondary">{item.description}</CardText>
                  </CardBody>
                </Link>
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