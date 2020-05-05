import React from "react";
import Wrapper from "./components/wrapper/wrapper";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import {toast, ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default class App extends React.Component {


  render() {
    return (
      <div className="App">
        <ToastContainer position={toast.POSITION.TOP_CENTER}/>
        <Wrapper/>
      </div>
    )
  };
}
