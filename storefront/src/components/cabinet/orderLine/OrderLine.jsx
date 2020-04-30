/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";
import {Button, Collapse, Modal, ModalBody, ModalFooter, ModalHeader} from "reactstrap";
import {GoPrimitiveDot} from "react-icons/go";
import {MdCancel} from "react-icons/md";
import {Table} from "react-bootstrap";
import axios from "axios";
import {toast} from "react-toastify";
import Auth from "../../auth/auth";

export default class OrderLine extends React.Component {
  /**
   * OrderLine constructor
   *
   * @param props
   */
  constructor(props) {
    super(props);
    this.state = {
      isOpen: false,
      modal: false
    }
    this.user = new Auth()
  }

  /**
   * Collapse toggler
   */
  toggle = () => {
    const {isOpen} = this.state;
    this.setState({
      isOpen: !isOpen
    });
  };

  toggleModal = (event) => {
    event.preventDefault();
    const {modal} = this.state;
    this.setState({
      modal: !modal
    });
  }

  deleteOrder = () => {
    axios(`${process.env.REACT_APP_CANCEL_ORDER}${this.props.data.pk}/`, {
      headers: {
        "Authorization": "Token " + this.user.getAuthToken(),
      }
    }).then((response) => {
      toast.success(response.data)
      this.setState({
        modal: false
      })
      this.props.refresh()
    })
      .catch((error) => {
        toast.error(error.response.data)
      })
  }


  render() {
    return (
      <>
        <tr style={{cursor: 'pointer'}} onClick={this.toggle}>
          <td className="text-center pt-1 pb-1">
            {this.props.data.invoice_number}
          </td>
          <td className="text-center pt-1 pb-1">
            {this.props.data.status === "NO" && <GoPrimitiveDot size={"1.5em"} color="orange"/>}
            {this.props.data.status === "CF" && <GoPrimitiveDot size={"1.5em"} color="green"/>}
            {this.props.data.status === "CN" && <GoPrimitiveDot size={"1.5em"} color="red"/>}
            {this.props.data.status === "RT" && <GoPrimitiveDot size={"1.5em"} color="grey"/>}
            {this.props.data.status_display}
          </td>
          <td className="text-center pt-1 pb-1">
            {this.props.data.date_created}
          </td>
          <td className="text-center pt-1 pb-1">
            {this.props.data.lenses_sum}
          </td>
          <td className="text-center pt-1 pb-1">
            {this.props.data.value} {process.env.REACT_APP_CURRENCY}
          </td>
          <td className="text-center pt-1 pb-1">{this.props.data.status === "NO" &&
          <a href="" onClick={this.toggleModal}>
            <MdCancel color="red"/>
          </a>
          }</td>
        </tr>

        <div>
          <Modal isOpen={this.state.modal} toggle={this.toggleModal} className="modal-lg">
            <ModalHeader toggle={this.toggleModal}>Видалити замовлення?</ModalHeader>
            <ModalBody>
              <h4>Деталі замовлення:</h4>
              <Table responsive bordered hover className="mb-0">
                <thead>
                <tr>
                  <th className="text-center">Номер замовлення</th>
                  <th className="text-center">Дата замовлення</th>
                  <th className="text-center">Кількість лінз</th>
                  <th className="text-center">Вартість</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                  <td className="text-center">{this.props.data.invoice_number}</td>
                  <td className="text-center">{this.props.data.date_created}</td>
                  <td className="text-center">{this.props.data.lenses_sum}</td>
                  <td className="text-center">{this.props.data.value}</td>
                </tr>
                </tbody>
              </Table>
              <h4>Вміст замовлення:</h4>
              <Table responsive bordered hover className="mb-0">
                <thead>
                <tr>
                  <th className="text-center">Назва</th>
                  <th className="text-center">Кількість лінз</th>
                  <th className="text-center">Ціна за одиницю</th>
                </tr>
                </thead>
                <tbody>
                {this.props.data.order_lines.map((orderItem) => (
                  <tr>
                    <td className="text-center">{orderItem.product}</td>
                    <td className="text-center">{orderItem.quantity}</td>
                    <td className="text-center">{orderItem.unit_price}</td>
                  </tr>
                ))}
                </tbody>
              </Table>
            </ModalBody>
            <ModalFooter>
              <Button color="primary" onClick={this.deleteOrder}>Гаразд</Button>{' '}
              <Button color="secondary" onClick={this.toggleModal}>Відміна</Button>
            </ModalFooter>
          </Modal>
        </div>

        {this.props.data.order_lines.map((orderItem) => (
          <>
            <Collapse tag="tr" className="bg-light" style={{backgroundColor: "#dddddd"}} colSpan={5}
                      isOpen={this.state.isOpen}>
              {Object.values(orderItem).map((item, index) => (
                <>
                  {index === 0 &&
                  <>
                    <td></td>
                    <td className="text-center pt-1 pb-1">
                      {item}
                    </td>
                  </>
                  }
                  {index === 1 &&
                  <>
                    <td className="text-center pt-1 pb-1">
                      {item}
                    </td>
                  </>
                  }
                  {index === 2 &&
                  <>
                    <td></td>
                    <td className="text-center pt-1 pb-1">
                      {item} {process.env.REACT_APP_CURRENCY}
                    </td>
                    <td width="2%"></td>
                  </>
                  }
                </>
              ))}
            </Collapse>
          </>

          // <ListGroup>
          //   <ListGroupItem style={{border: 'none'}} className="justify-content-between border-bottom text-center">
          //     Назва продукту <Badge color={'secondary'} pill className="mr-4">{orderItem.product}</Badge>
          //     Кількість <Badge color={'secondary'} pill className="mr-4">{orderItem.quantity}</Badge>
          //     Ціна за одиницю <Badge color={'secondary'} pill
          //                            className="mr-4">{orderItem.unit_price} {process.env.REACT_APP_CURRENCY}</Badge>
          //   </ListGroupItem>
          // </ListGroup>
        ))}


      </>
    )
  }
}
