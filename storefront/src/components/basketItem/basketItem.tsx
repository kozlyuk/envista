/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React, {Fragment} from "react";
import Auth from "../auth/auth";
import BasketInputNumber from "../basketInputNumber/basketInputNumber";
import axios from "axios";
import "../basketItem/style.css"
import {toast} from "react-toastify";
import {Button, Col, Row, Table} from "react-bootstrap";

/*
 * State interface
 */
interface BasketItemState {
  array?: any
  error?: any
  isLoaded?: boolean
  maxQuantity?: number
  isBasketActive?: boolean
  availableorders?: any
  orders_total?: number
  preorders?: any
  preorders_total?: number
}

export default class BasketItem extends React.Component<{}, BasketItemState> {
  private user: Auth;
  private authToken: any;

  constructor(props: any, state: any) {
    super(props, state);
    this.state = {
      array: null,
      error: null,
      isLoaded: false,
      maxQuantity: 0,
      isBasketActive: true,
      availableorders: null,
      orders_total: undefined,
      preorders: null,
      preorders_total: undefined
    };
    this.preOrderCell = this.preOrderCell.bind(this);
    this.orderCell = this.orderCell.bind(this);
    this.user = new Auth();
    this.authToken = this.user.getAuthToken();
  }

  /*
   * BasketItem.updateQuantity(value)
   *
   * Middleware reducer.
   * Need to catch value from child component, and put to parent state
   * return same data as input
   */
  updateQuantity(value: number) {
    return value
  }

  /*
   * BasketItem.cell(colIdx:number, rowIdx:number, item:object): React.Component
   *
   * Filter method for cell in table
   */
  orderCell(colIdx: number, rowIdx: number, item: any) {
    if (colIdx === 4) {
      return (<BasketInputNumber colIdx={colIdx} rowIdx={rowIdx} item={item} orderArray={this.state.availableorders}
                                 updateQuantity={this.updateQuantity}/>)
    } else if (colIdx === 5) {
      return void 0
    } else if (colIdx === 6 || colIdx === 7) {
      return void 0
    } else {
      return (<td key={colIdx}>{item}</td>)
    }
  }

  /*
   * BasketItem.cell(colIdx:number, rowIdx:number, item:object): React.Component
   *
   * Filter method for cell in table
   */
  preOrderCell(colIdx: number, rowIdx: number, item: any) {
    if (colIdx === 4) {
      return (<BasketInputNumber colIdx={colIdx} rowIdx={rowIdx} item={item} orderArray={this.state.preorders}
                                 updateQuantity={this.updateQuantity} preOrder/>)
    } else if (colIdx === 5) {
      return void 0
    } else if (colIdx === 6 || colIdx === 7) {
      return void 0
    } else {
      return (<td key={colIdx}>{item}</td>)
    }
  }

  /*
   * BasketItem.handleClick(): void
   *
   * Method handler
   * When success - confirm order and put response to state
   * When error - drop error toast
   */
  handleClick() {
    const {REACT_APP_CONFIRM_ORDER}: any = process.env;
    axios(REACT_APP_CONFIRM_ORDER, {
      headers: {
        "Authorization": "Token " + this.authToken
      }
    }).then((response: any) => {
      this.setState({
        array: [],
        isBasketActive: false
      });
      // toast.success(response.data)
    }).catch((error: any) => {
      const message: any = error.data;
      if (error.response.status === 412) {
        this.setState({
          array: []  // if error status 412 clear data
        })
      }
      toast.error(error.response);
    })
  }

  _loadData() {
    const {REACT_APP_BASKET_DATA_URL}: any = process.env;
    axios(REACT_APP_BASKET_DATA_URL, {
      headers: {
        "Authorization": "Token " + this.authToken
      }
    })
      // .then(res => res.json())
      .then(
        (result: any) => {
          this.setState({
            isLoaded: true,
            array: result.data
          });
          this._reformatJson()
        },
        (error: any) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      );
    return void 0;
  }

  _reformatJson() {
    this.state.array.map((items: { availableorders: any, orders_total: number, preorders: any, preorders_total: number }) => {
      if (items.availableorders) {
        this.setState({
          availableorders: Object.entries(items.availableorders)
        })
      } else if (items.orders_total) {
        this.setState({
          orders_total: items.orders_total
        })
      } else if (items.preorders) {
        this.setState({
          preorders: Object.entries(items.preorders)
        })
      } else if (items.preorders_total) {
        this.setState({
          preorders_total: items.preorders_total
        })
      }
    })
  }

  /*
   * BasketItem.componentDidMount()
   * Called immediately after a component is mounted. Setting state here will trigger re-rendering.
   * Get data from API
   * While error - drop error
   */
  componentDidMount() {
    this._loadData()
  }

  render() {
    const {error, isLoaded}: any = this.state;
    if (error) {
      return <h3 className="text-center">Помилка: {error.message}</h3>;
    } else if (!isLoaded) {
      return <h3 className="text-center">Завантаження...</h3>;
    } else if (!this.state.isBasketActive) {
      return (
        <div className="mt-4">
          <div className="checkmark-circle ml-auto mr-auto">
            <div className="background"></div>
            <div className="checkmark draw"></div>
          </div>
          <h3 className="text-success text-center">Дякуємо за покупку!</h3>
        </div>
      )
    } else if (!this.state.orders_total && !this.state.preorders_total) {
      return <h3 className="text-center">У вас не має замовлень в корзині</h3>;
    } else {
      console.log(this.state.orders_total && this.state.preorders_total)
      return (
        <Fragment>
          <Row>
            <Col className="text-center">
              <h2 className="text-muted">Корзина</h2>
            </Col>
          </Row>
          <Row>
            <Col>
              <h4 className="text-center">Ваші замовлення</h4>
              <Table responsive striped bordered hover className="mb-0">
                <thead>
                <tr>
                  <th>#</th>
                  <th>Назва</th>
                  <th>Сфера</th>
                  <th>Циліндр</th>
                  <th className="text-center">Кількість</th>
                  <th>Вартість</th>
                </tr>
                </thead>
                <tbody>
                {this.state.availableorders &&
                this.state.availableorders.map((items: any, rowIdx: number) => (
                  <tr>
                    {items[1].line.map((item: any, colIdx: any) => (
                      this.orderCell(colIdx, rowIdx, item)
                    ))}
                  </tr>
                ))
                }
                {this.state.preorders &&
                (
                  <th className="text-center" colSpan={6}>Попереднє замовлення</th>
                )}
                {this.state.preorders && this.state.preorders.map((items: any, rowIdx: number) => (
                  <tr>
                    {items[1].line.map((item: any, colIdx: any) => (
                      this.preOrderCell(colIdx, rowIdx, item)
                    ))}
                  </tr>
                ))}
                </tbody>
              </Table>
              <div className="text-center mt-4">
                <Button
                  variant="outline-success"
                  size="sm"
                  onClick={() => {
                    this.handleClick();
                  }}>
                  Підтвердити замовлення
                </Button>
              </div>
            </Col>
          </Row>
        </Fragment>
      )
    }
  }
}
