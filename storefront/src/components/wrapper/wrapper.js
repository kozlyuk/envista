/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";
import Content from "../content/content";

import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import Basket from "../basket/basket";
import Auth from "../auth/auth";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"
import axios from "axios";
import Warehouse from "../warehouse/warehouse";
import WarehouseConfirm from "../warehouseConfirm/warehouseConfirm";
import {Redirect} from "react-router";
import Cabinet from "../cabinet/Cabinet";
import Loader from "react-loader-spinner";
import Login from "../auth/login";
import Registration from "../auth/registration";
import Activation from "../auth/Activation";
import LayoutRoute from "../../layouts/LayoutRoute";
import StorefrontLayout from "../../layouts/StorefrontLayout";
import {GlobalContext} from "../../context/GlobalContext";
import DashboardApp from "../../DashboardEntryPoint";

class Wrapper extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoading: true,
      isAuthenticate: false,
      user: null,
      permission: null
    };
    this.user = new Auth();
    this.getDataFromChild = this.getDataFromChild.bind(this)
  }

  /**
   * Collect permisions
   *
   * @param permissions
   * @private
   */
  _collectPermissions(permissions) {
    let permission = []
    permissions.map((perm) => {
      permission.push(perm.name)
    })
    this.setState({
      permission: permission
    })
  }

  /*
   * Welcome.componentDidMount(): void
   *
   * Called immediately after a component is mounted.
   * Setting state here will trigger re-rendering.
   * Get user from API
   * When success write in state isAuthenticate: true
   * and user data
   * When error write in state isAuthenticate: false
   * and redirect to login page
   */
  componentDidMount() {
    axios(process.env.REACT_APP_USER_DATA, {
      headers: {
        "Authorization": "Token " + this.user.getAuthToken(),
      }
    })
      .then(
        (response) => {
          if (response.status >= 400) {
            this.setState({
              isAuthenticate: false,
            })
          } else if (response.status < 400) {
            this.setState({
              isAuthenticate: true,
              user: response.data
            })
            this._collectPermissions(response.data.groups)
          }
        });
    setTimeout(() => {
      this.setState({
        isLoading: false
      })
    }, 1000)
  }

  /*
   * Welcome.getDataFromChild(data?):void
   *
   * method initiator for child component
   * get from child props with brand logo and write to state
   */
  getDataFromChild(brandLogo, footer) {
    (this.setState({
      brandLogo: brandLogo,
      footer: footer
    }));
    return void 0
  }

  render() {
    if (this.state.isLoading) {
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
        </div>);
    } else if (this.state.isAuthenticate) {
      return (
        <header className="main-container">
          <div>
            <GlobalContext.Provider
              value={{
                user: this.state.user,
                brandLogo: this.state.brandLogo,
                permission: this.state.permission,
                footer: this.state.footer
              }}>
              <Router>
                <Switch>
                  <LayoutRoute
                    exact path="/basket" layout={StorefrontLayout}
                    component={(props) => (<Basket/>)}
                  />
                  <LayoutRoute
                    exact path="/cabinet" layout={StorefrontLayout}
                    component={(props) => (<Cabinet userPk={this.state.user.pk}/>)}
                  />
                  <Route exact path="/dashboard" component={DashboardApp}/>
                  <LayoutRoute
                    exact path="/warehouse/confirm" layout={StorefrontLayout}
                    component={(props) => (
                      this.state.permission.includes('Менеджери') ?
                        <WarehouseConfirm/> :
                        <h3 className="text-center text-muted"> На жаль у Вас не має дозволу
                          для
                          перегляду
                          сторінки</h3>
                    )}
                  />
                  <LayoutRoute
                    exact path="/warehouse" layout={StorefrontLayout}
                    component={(props) => (
                      this.state.permission.includes('Менеджери') ?
                        <Warehouse/> :
                        < h3 className="text-center text-muted"> На жаль у Вас не має дозволу
                          для
                          перегляду
                          сторінки</h3>
                    )}
                  />
                  <LayoutRoute
                    exact path="/" layout={StorefrontLayout}
                    component={(props) => (<Content getData={() => this.getDataFromChild}/>)}
                  />
                  <Route exact path="/not_found" render={() => {
                    window.location.href = "404.html"
                  }}/>
                  <Redirect to="/not_found"/>
                </Switch>
              </Router>
            </GlobalContext.Provider>
          </div>
        </header>)
    } else {
      return (
        <Router>
          <Switch>
            <Route exact path="/">
              <Login/>
            </Route>
            <Route exact path="/registration" component={props => (
              <Registration {...props}/>
            )}>
            </Route>
            <Route exact path="/activation/:uidb64/:token" component={props => (
              <Activation {...props}/>
            )}>
            </Route>
            <Route exact path="/not_found" render={() => {
              window.location.href = "404.html"
            }}/>
            <Redirect to="/not_found"/>
          </Switch>
        </Router>
      )
    }
  }
}

export default Wrapper;
