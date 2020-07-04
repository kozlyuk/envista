import React from 'react';
import $ from 'jquery';
import Categories from "./dashboardViews/categories/Categories";
import ProductList from "./dashboardViews/product/ProductList";

window.jQuery = $;
window.$ = $;
global.jQuery = $;

const DashboardDefault = React.lazy(() => import('./Demo/Dashboard/Default'));

const routes = [
  {path: '/', exact: true, name: 'Default', component: DashboardDefault},
  {path: '/categories', exact: true, name: 'Categories', component: Categories},
  {path: '/products', exact: true, name: 'Products', component: ProductList},
];

export default routes;