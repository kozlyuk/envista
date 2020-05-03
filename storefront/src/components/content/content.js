/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";

import {Table} from "../table/table.tsx";
import Submit from "../submitTableData/submitTableData";
import PurchaseList from "../purchaseList/purchaseList";
import InfoBlock from "../infoBlock/infoBlock.tsx";
import {Container} from "react-bootstrap";
import axios from "axios";
import Auth from "../auth/auth";
import Loader from "react-loader-spinner";
import PreOrderList from "../preOrderList/preOrderList";

export default class Content extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      purchase: [],
      preOrder: [],
      array: [],
      preOrderArray: []
    };
    this.user = new Auth();
    this.authToken = this.user.getAuthToken();
  }

  //get data from child component and put into state
  makePurchase = purchase => {
    this.setState(prevState => ({
      purchase: [...prevState.purchase, purchase]
    }));
  };

  //get data from child component and put into state
  makePreOrder = preOrder => {
    console.log("test2")
    this.setState(prevState => ({
      preOrder: [...prevState.preOrder, preOrder]
    }));
  };

  //get table data from child component and put into state
  getArray = array => {
    this.setState(prevState => ({
      array: [...prevState.array, array]
    }));
  };

  //get pre order table data from child component and put into state
  getPreOrderArray = preOrderArray => {
    this.setState(prevState => ({
      array: [...prevState.preOrderArray, preOrderArray]
    }));
  };

  componentDidMount() {
    axios(process.env.REACT_APP_INFO_CONTEXT, {
      headers: {
        Authorization: "Token " + this.authToken
      }
    }).then(
      result => {
        this.setState({
          isLoaded: true,
          product: result.data
        });
        this.props.getData(this.state.product.brand_image, this.state.product.footer);
      },
      error => {
        this.setState({
          isLoaded: true,
          error
        });
      }
    );
    return void 0;
  }

  render() {
    const {error, isLoaded} = this.state;
    if (error) {
      return <div>Помилка: {error.message}</div>;
    } else if (!isLoaded) {
      return (
        <div className="loaderWrapper text-center mt-4">
          <Loader
            type="MutatingDots"
            color="#007bff"
            height={100}
            width={100}
            timeout={3000} //3 secs

          />
          <h3 className="text-center text-muted">Завантаження...</h3>
        </div>
      );
    } else {
      return (
        <Container>
          <div className="w-row">
            <div className="mobile-second w-col w-col-6">
              {/* Header */}
              <h1 className="heading mt-0">
                <strong className="bold-text" data-ix="new-interaction">
                  {this.state.product.title}
                </strong>
              </h1>
              {/* End of header */}
              <img
                src={this.state.product.product_image}
                alt={this.state.product.title}
                className="image-3"
              />

              <InfoBlock info={this.state.product.short_description}
                         pdfUrl={this.state.product.specifications_url}
                         telegram_bot_url={this.state.product.telegram_bot_url}
              />
            </div>
            <div className="mobile-first w-col w-col-6">
              <h4 className="text-center">Таблиця наявності лінз на складі</h4>
              <Table getData={this.makePurchase} getPreOrderData={this.makePreOrder} getArray={this.getArray}
                     getPreOrderArray={this.getPreOrderArray}/>
              <PurchaseList
                purchaseList={this.state.purchase}
                array={this.state.array}
              />
              <PreOrderList
                preOrderList={this.state.preOrder}
                array={this.state.array}
              />
              {this.state.purchase.length !== 0 || this.state.preOrder.length ? (
                <Submit history={this.history} title={"Перейти в корзину"} redirectTo={"/basket"}/>
              ) : ''}
            </div>
          </div>
        </Container>
      );
    }
  }
}
