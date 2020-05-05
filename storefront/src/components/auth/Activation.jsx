/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";
import axios from "axios";
import {Container} from "react-bootstrap";
import {Button, Row} from "reactstrap";
import {Link} from "react-router-dom";
import {AiOutlineCloseCircle} from 'react-icons/ai';

export default class Activation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      successResponse: false,
      errorResponse: false
    }
  }

  componentDidMount() {
    axios(`${process.env.REACT_APP_ACTIVATION}${this.props.match.params.uidb64}/${this.props.match.params.token}/`)
      .then((response) => {
        this.setState({
          successResponse: response.data
        })
      }).catch((error) => {
      this.setState({
        errorResponse: error.response.data
      })
    })
  }

  render() {
    return (
      <Container>
        {this.state.successResponse &&
        <>
          <div className="mt-4">
            <div className="checkmark-circle ml-auto mr-auto">
              <div className="background"></div>
              <div className="checkmark draw"></div>
            </div>
            <h3 className="text-success text-center">{this.state.successResponse}</h3>
            <Row>
              <Link className="mx-auto" to="/">
                <Button className="btn-success">
                  Перейти до сторінки входу
                </Button>
              </Link>
            </Row>
          </div>
        </>
        }
        {this.state.errorResponse &&
        <>
          <div className="mt-4">
            <div className="checkmark-circle ml-auto mr-auto">
              <AiOutlineCloseCircle className="text-danger" size={"10em"}/>
            </div>
            <h3 className="text-danger text-center">{this.state.errorResponse}</h3>
          </div>
        </>
        }
      </Container>
    )
  }
}