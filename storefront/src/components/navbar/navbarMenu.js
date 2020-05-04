/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React, {Fragment} from "react";
import {Link} from "react-router-dom";
import Auth from "../auth/auth";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import axios from "axios";

class NavbarMenu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      brand_image: null
    };
    this.user = new Auth();
    this.authToken = this.user.getAuthToken();
  }


  /**
   * @return {*}
   */
  componentDidMount() {
    axios(process.env.REACT_APP_INFO_CONTEXT, {
      headers: {
        Authorization: "Token " + this.authToken
      }
    }).then(
      result => {
        this.setState({
          brand_image: result.data.brand_image
        });
      },
      error => {
        this.setState({
          error
        });
      }
    );
    return void 0;
  }

  render() {
    return (
      <Fragment>
        <div>
          <Navbar collapseOnSelect expand="lg" className="top-nav">
            <div className="container">
              <Navbar.Brand href="#home"><Link to="/" className="mr-auto m-0 brand w-nav-brand p-0">
                <img
                  src={this.state.brand_image}
                  height={50}
                  alt="brand"
                  className="image-2"
                />
              </Link></Navbar.Brand>
              <Navbar.Toggle aria-controls="responsive-navbar-nav"/>
              <Navbar.Collapse id="responsive-navbar-nav" className="menu-list">
                <Nav className="ml-auto">
                  <Link style={{color: "#222222", padding: "20px"}} to="/">
                    Головна
                  </Link>
                  {this.props.permission.includes('Менеджери') ? <Link
                    style={{
                      maxWidth: 940,
                      color: "#222222",
                      display: "inline-block",
                      padding: "20px"
                    }}
                    to="/warehouse">
                    Поповнення складу
                  </Link> : ""}
                  <Link
                    style={{
                      maxWidth: 940,
                      color: "#222222",
                      display: "inline-block",
                      padding: "20px"
                    }}
                    to="/basket">
                    Корзина
                  </Link>
                  <Link
                    style={{
                      maxWidth: 940,
                      color: "#222222",
                      display: "inline-block",
                      padding: "20px"
                    }}
                    to="/cabinet">
                    Особистий кабінет
                  </Link>
                  <Link
                    style={{
                      maxWidth: 940,
                      color: "#222222",
                      display: "inline-block",
                      padding: "20px"
                    }}
                    to="/logout"
                    onClick={() => {
                      this.user.logout().then(() => {
                        window.location.assign('/');
                      });
                    }}>
                    Вийти ({this.props.userEmail})
                  </Link>
                </Nav>
              </Navbar.Collapse>
            </div>
          </Navbar>
        </div>

      </Fragment>
    )
  }
}

export default NavbarMenu;
