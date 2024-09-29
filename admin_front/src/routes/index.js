import React from 'react';
import LoginPage from "../views/LoginPage";
import RegisterPage from "../views/RegisterPage";
import Home from "../views/Home";

const routes = [
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/register',
    element: <RegisterPage />,
  },
];

export default routes;
