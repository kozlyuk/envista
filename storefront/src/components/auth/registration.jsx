/**
 * @author    Andrey Perestyuk (Arrathilar) a.perestyuk@itel.rv.ua
 * @copyright 2020 ITEL-Service
 */

import React from "react";
import {Container} from "react-bootstrap";
import {Link} from "react-router-dom";
import axios from 'axios';
import Auth from "./auth";
import {toast} from "react-toastify";
import FieldError from "../errorContainers/fieldError";
import {Button, Modal, ModalBody, ModalFooter, ModalHeader} from "reactstrap";
import ContentPolicy from "./contentPolicy";

/**
 * Ugly regular expression for validate length of phone number
 *
 * @type {RegExp}
 */
const validPhoneRegex = RegExp(/\(?([0-9]{3})\)?([ .-]?)([0-9]{3})\2([0-9]{4})/);

/**
 * Ugly regular expression for validate email
 *
 * @type {RegExp}
 */
const validEmailRegex = RegExp(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/);

export default class Registration extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      password: '',
      errors: {
        first_name: null,
        last_name: null,
        email: null,
        mobile_number: null,
        password: null,
        password2: null
      },
      fieldError: {
        first_name: null,
        last_name: null,
        email: null,
        mobile_number: null,
        password: null
      }
    }
    this.user = new Auth();
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleChange = (event) => {
    event.preventDefault();
    const {name, value} = event.target;
    let errors = this.state.errors;

    if (name === "password") {
      this.setState({
        password: value
      })
    }

    switch (name) {
      case 'mobile_number':
        errors.mobile_number =
          validPhoneRegex.test(value)
            ? ''
            : 'Номер телефону має не вірний формат!';
        break;
      case 'email':
        errors.email =
          validEmailRegex.test(value)
            ? ''
            : 'Email має невірний формат!';
        break;
      case 'first_name':
        errors.first_name =
          value.length > 0
            ? ''
            : 'Це поле обов\'язкове!';
        break;
      case 'last_name':
        errors.last_name =
          value.length > 0
            ? ''
            : 'Це поле обов\'язкове!';
        break;
      case 'password':
        errors.password =
          value.length < 6
            ? 'Пароль повинен бути не менше 6 символів!'
            : '';
        break;
      case 'password2':
        errors.password2 =
          value !== this.state.password
            ? 'Паролі повинні співпадати!'
            : '';
        break;
      default:
        break;
    }

    this.setState({errors, [name]: value});
  };

  /**
   *
   * @param event
   * @return {FormData}
   */
  submitData(event) {
    const form = document.forms.registration
    const userFormData = new FormData(form);
    const userEmail = form.email.value.toLowerCase();
    userFormData.delete('password2')
    userFormData.set('email', userEmail);
    return userFormData;
  }

  /**
   *
   * @param event
   */
  handleSubmit(event) {
    event.preventDefault();
    axios({
      method: "post",
      url: process.env.REACT_APP_REGISTRATION,
      data: this.submitData(event)
    }).then((data) => {
      toast.success(data.data, {onClose: this.props.history.push('/')})
    }).catch((error) => {
      this.setState({
        fieldError: error.response.data
      })
    })
  }

  render() {
    return (
      <Container className="auth-container sm-container">
        <div style={{height: "100%"}} className="box">
          <form id="registration" onSubmit={this.handleSubmit}>
            <h1>Реєстрація</h1>
            <div className="group sm-group">
              <input onChange={this.handleChange} id="first_name" name="first_name" className="inputMaterial"
                     type="text" required/>
              {this.state.fieldError.first_name &&
              <FieldError error={this.state.fieldError.first_name}/>
              }
              {this.state.errors.first_name &&
              <FieldError error={this.state.errors.first_name}/>
              }
              <span className="highlight"/>
              <span className="bar"/>
              <label style={{top: "-20px"}}>Ім'я</label>
            </div>
            <div className="group sm-group">
              <input onChange={this.handleChange} id="last_name" name="last_name" className="inputMaterial" type="text"
                     required/>
              {this.state.fieldError.last_name &&
              <FieldError error={this.state.fieldError.last_name}/>
              }
              {this.state.errors.last_name &&
              <FieldError error={this.state.errors.last_name}/>
              }
              <span className="highlight"/>
              <span className="bar"/>
              <label style={{top: "-20px"}}>Прізвище</label>
            </div>
            <div className="group sm-group">
              <input onChange={this.handleChange} id="email" name="email" className="inputMaterial" type="email"
                     required/>
              {this.state.fieldError.email &&
              <FieldError error={this.state.fieldError.email}/>
              }
              {this.state.errors.email &&
              <FieldError error={this.state.errors.email}/>
              }
              <span className="highlight"/>
              <span className="bar"/>
              <label style={{top: "-20px"}}>Пошта</label>
            </div>
            <div className="group sm-group">
              <input onChange={this.handleChange} id="mobile_number" name="mobile_number" className="inputMaterial"
                     type="phone" required/>
              {this.state.fieldError.mobile_number &&
              <FieldError error={this.state.fieldError.mobile_number}/>
              }
              {this.state.errors.mobile_number &&
              <FieldError error={this.state.errors.mobile_number}/>
              }
              <span className="highlight"/>
              <span className="bar"/>
              <label style={{top: "-20px"}}>Номер телефону</label>
            </div>
            <div className="group sm-group">
              <input onChange={this.handleChange} id="password" name="password" className="inputMaterial"
                     type="password" required/>
              {this.state.fieldError.password &&
              <FieldError error={this.state.fieldError.password}/>
              }
              {this.state.errors.password &&
              <FieldError error={this.state.errors.password}/>
              }
              <span className="highlight"/>
              <span className="bar"/>
              <label style={{top: "-20px"}}>Пароль</label>
            </div>
            <div className="group sm-group">
              <input onChange={this.handleChange} id="password2" name="password2" className="inputMaterial"
                     type="password" required/>
              {this.state.fieldError.password2 &&
              <FieldError error={this.state.fieldError.password2}/>
              }
              {this.state.errors.password2 &&
              <FieldError error={this.state.errors.password2}/>
              }
              <span className="highlight"/>
              <span className="bar"/>
              <label style={{top: "-20px"}}>Підтвердження паролю</label>
            </div>
            <button type="submit" id="buttonlogintoregister">Зареєструватися</button>
            <Link to="/" style={{textDecoration: 'none'}}>
              <button className="bg-info" type="button">Повернутися до сторінки входу</button>
            </Link>
          </form>
        </div>
      </Container>
    )
  }
}
