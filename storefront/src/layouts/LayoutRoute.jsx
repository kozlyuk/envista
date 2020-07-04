/*
 * @author     Andrey Perestyuk (Arrathilar)
 * @email       a.perestyuk@itel.rv.ua
 * @email       arrathilar@blizzard.com, a.perestyuk@archlinux.org,
 * @copyright  2020 ITEL-Service
 *
 */

import React from 'react';
import {Route} from 'react-router-dom';

const LayoutRoute = ({component: Component, layout: Layout, ...rest}) => (
  <Route
    {...rest}
    render={props => (
      <Layout>
        <Component {...props} />
      </Layout>
    )}
  />
);

export default LayoutRoute;