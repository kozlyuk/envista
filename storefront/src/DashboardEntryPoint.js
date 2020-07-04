/*
 * @author     Andrey Perestyuk (Arrathilar)
 * @email       a.perestyuk@itel.rv.ua
 * @email       arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright  2020 ITEL-Service
 *
 */

import React from "react";
import {createStore} from 'redux';
import {Provider} from 'react-redux';
import {BrowserRouter} from "react-router-dom";

import App from './App/index'
import reducer from './store/reducer';
import config from "./config";

const store = createStore(reducer);

function DashboardApp() {
  return (
    <Provider store={store}>
      <BrowserRouter basename={config.basename}>
        <App/>
      </BrowserRouter>
    </Provider>
  )
}

export default DashboardApp;