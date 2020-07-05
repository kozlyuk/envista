import React, {Component} from 'react';
import {Dropdown} from 'react-bootstrap';

import ChatList from './ChatList';
import Aux from "../../../../../hoc/_Aux";
import DEMO from "../../../../../store/constant";

import Avatar1 from '../../../../../assets/images/user/avatar-1.jpg';
import {GlobalContext} from "../../../../../context/GlobalContext";

class NavRight extends Component {
  state = {
    listOpen: false
  };

  render() {

    return (
      <Aux>
        <ul className="navbar-nav ml-auto">
          <li className={this.props.rtlLayout ? 'm-r-15' : 'm-l-15'}>
            <a href={DEMO.BLANK_LINK} className="displayChatbox" onClick={() => {
              this.setState({listOpen: true});
            }}><i className="icon feather icon-mail"/></a>
          </li>
          <li>
            <Dropdown alignRight={!this.props.rtlLayout} className="drp-user">
              <Dropdown.Toggle variant={'link'} id="dropdown-basic">
                <i className="icon feather icon-settings"/>
              </Dropdown.Toggle>
              <Dropdown.Menu alignRight className="profile-notification">
                <GlobalContext.Consumer>
                  {({user}) => (
                    <>
                      <div className="pro-head">
                        <img src={Avatar1} className="img-radius" alt="User Profile"/>
                        <span>{user.first_name} {user.last_name}</span>
                      </div>
                      <ul className="pro-body">
                        <li>
                          <a href={DEMO.BLANK_LINK} className="dropdown-item">
                            <i className="feather icon-user"/>Профіль
                          </a>
                        </li>
                        <li>
                          <a href={DEMO.BLANK_LINK} className="dropdown-item"><i className="feather icon-log-out"/>
                            Вийти
                          </a>
                        </li>
                      </ul>
                    </>
                  )}
                </GlobalContext.Consumer>
              </Dropdown.Menu>
            </Dropdown>
          </li>
        </ul>
        <ChatList listOpen={this.state.listOpen} closed={() => {
          this.setState({listOpen: false});
        }}/>
      </Aux>
    );
  }
}

export default NavRight;
