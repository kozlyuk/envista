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
      checkedPolicy: false,
      modal: false,
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
    this.handlePolicyChange = this.handlePolicyChange.bind(this)
    this.toggleModal = this.toggleModal.bind(this)
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

  toggleModal() {
    this.setState({
      modal: !this.state.modal
    })
  }

  handlePolicyChange() {
    this.setState({
      checkedPolicy: !this.state.checkedPolicy
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
            <div className="checkbox-group sm-group">

              <div className="checkbox-wrapper">
                <input style={{float: "left", width: "40px", height: "18px"}} id="policy" name="policy"
                       className="inputMaterial"
                       checked={this.state.checkedPolicy}
                       onChange={this.handlePolicyChange}
                       type="checkbox" required/>
                <div className="m-0" style={{top: "-20px", fontSize: "11px"}}>
                  Я погоджуюся на <a
                  onClick={this.toggleModal}
                  style={{color: "blue", cursor: "pointer"}}
                > обробку
                  персональних даних.</a>
                </div>

              </div>
            </div>
            {this.state.checkedPolicy ?
              <button type="submit" id="buttonlogintoregister">Зареєструватися</button>
              :
              <button type="button" style={{backgroundColor: "grey"}}
                      id="buttonlogintoregister">Потрібно підтвердження на обробку данних</button>
            }
            <Link to="/" style={{textDecoration: 'none'}}>
              <button className="bg-info" type="button">Повернутися до сторінки входу</button>
            </Link>
          </form>
        </div>
        <Modal isOpen={this.state.modal} toggle={this.toggleModal} className="modal-xl">
          <ModalHeader toggle={this.toggleModal}>Згода на обробку персональних даних</ModalHeader>
          <ModalBody>
            {contentPolicy}
          </ModalBody>
          <ModalFooter>
            <Button color="secondary" onClick={this.toggleModal}>Закрити</Button>
          </ModalFooter>
        </Modal>
      </Container>
    )
  }
}

const contentPolicy = (
  <>
    <p>
      Надаю Товариству з обмеженою відповідальністю «Бауш Хелс» (далі – Володілець) добровільну та безумовну згоду на
      обробку моїх персональних даних, а саме: прізвища, імені, по батькові, дати і року народження, номер мобільного
      телефону, адресу електронної пошти в наступних цілях:
    </p>
    <p>
      • Для інформування про проведення і (або) організації моєї участі в науково-практичних або освітніх заходах у
      сфері охорони здоров'я та фармацевтики, а також заходах, спрямованих на інформування медичних і фармацевтичних
      працівників про продукцію групи компаній Бауш Хелс;
    </p>
    <p>
      • Для поширення наукової, освітньої, рекламної та іншої інформації;
    </p>
    <p>
      • Для проведення маркетингових досліджень, опитувань, інших заходів і оцінки задоволеності якістю продукції групи
      компаній Бауш Хелс.
    </p>
    <p>
      Я надаю згоду, що зазначена вище інформація може надаватися мені за електронною поштою, так і за телефоном
      (дзвінок/SMS/месенджер)
      Я надаю безумовну згоду на будь-які дії по обробці моїх персональних даних в документальній та / або електронній
      формі (включаючи, але не обмежуючись, збір, запис, систематизацію, накопичення, зберігання, уточнення (оновлення,
      зміну), використання, знеособлення, блокування, видалення, знищення персональних даних; на надання часткового або
      повного права обробки моїх персональних даних іншим суб'єктам відносин, пов'язаних із персональними даними (у тому
      числі й іноземним); на передачу будь-яким особам (у тому числі й іноземним) відомостей про мене з баз персональних
      даних (поширення персональних даних) без окремих дозволів та письмових повідомлень мене про це відповідно
      внутрішніх нормативних документів Володільця.
      Я надаю безумовну згоду на безстрокове зберігання моїх персональних даних та на те, що порядок доступу третіх осіб
      до моїх персональних даних буде визначений самостійно Володільцем персональних даних, а також на внесення змін до
      моїх персональних даних за зверненням інших суб'єктів відносин, пов'язаних із персональними даними без окремих
      дозволів та письмових повідомлень мене про це.
      Відповідно до ч.2 ст. 12 Закону України «Про захист персональних даних» повідомлений, про те, що: Володільцем
      персональних даних є ТОВ «БАУШ ХЕЛС» 01033, м. Київ, вул. Підвисоцького, 6В, тел. (044) 459 04 84 .
      Склад та зміст зібраних персональних даних, мета збору персональних даних осіб, яким передаються його персональні
      дані вказується у даній згоді, та є актуальним та дійсними на момент надання згоди.
      Про свої права відповідно до статті 8 Закону України «Про захист персональних даних» від 01.06.2010 № 2297-VI
      повідомлений Права суб’єкта персональних даних у сфері захисту персональних даних
    </p>
    <p>
      Відповідно до статті 8 Закону України «Про захист персональних даних» від 01.06.2010 № 2297-VI
    </p>
    <p>
      Особисті немайнові права на персональні дані, які має кожна фізична особа, є невід’ємними і непорушними.
      <p>
        Суб'єкт персональних даних має право:
      </p>
      <p>
        1) знати про джерела збирання, місцезнаходження своїх персональних даних, мету їх обробки, місцезнаходження або
        місце проживання (перебування) володільця чи розпорядника персональних даних або дати відповідне доручення щодо
        отримання цієї інформації уповноваженим ним особам, крім випадків, встановлених законом;
      </p>
      <p>
        2) отримувати інформацію про умови надання доступу до персональних даних, зокрема інформацію про третіх осіб,
        яким
        передаються його персональні дані;
      </p>
      <p>
        3) на доступ до своїх персональних даних;
      </p>
      <p>
        4) отримувати не пізніш як за тридцять календарних днів з дня надходження запиту, крім випадків, передбачених
        законом, відповідь про те, чи обробляються його персональні дані, а також отримувати зміст таких персональних
        даних;
      </p>
      <p>
        5) пред'являти вмотивовану вимогу володільцю персональних даних із запереченням проти обробки своїх персональних
        даних;
      </p>
      <p>
        6) пред'являти вмотивовану вимогу щодо зміни або знищення своїх персональних даних будь-яким володільцем та
        розпорядником персональних даних, якщо ці дані обробляються незаконно чи є недостовірними;
      </p>
      <p>
        7) на захист своїх персональних даних від незаконної обробки та випадкової втрати, знищення, пошкодження у
        зв'язку
        з умисним приховуванням, ненаданням чи несвоєчасним їх наданням, а також на захист від надання відомостей, що є
        недостовірними чи ганьблять честь, гідність та ділову репутацію фізичної особи;
      </p>
      <p>
        8) звертатися із скаргами на обробку своїх персональних даних до Уповноваженого або до суду;
      </p>
      <p>
        9) застосовувати засоби правового захисту в разі порушення законодавства про захист персональних даних;
      </p>
      <p>
        10) вносити застереження стосовно обмеження права на обробку своїх персональних даних під час надання згоди;
      </p>
      <p>
        11) відкликати згоду на обробку персональних даних;
      </p>
      <p>
        12) знати механізм автоматичної обробки персональних даних;
      </p>
      <p>
        13) на захист від автоматизованого рішення, яке має для нього правові наслідки.
      </p>
    </p>
  </>
)
