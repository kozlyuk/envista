import React from 'react';
import $ from 'jquery';
import Categories from "./dashboardViews/categories/Categories";

window.jQuery = $;
window.$ = $;
global.jQuery = $;

const DashboardDefault = React.lazy(() => import('./Demo/Dashboard/Default'));

const routes = [
  {path: '/', exact: true, name: 'Default', component: DashboardDefault},
  {path: '/categories', exact: true, name: 'Default', component: Categories},
];

export default routes;