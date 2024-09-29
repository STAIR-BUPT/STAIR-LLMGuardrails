import React, { Suspense } from 'react';
import { ConfigProvider } from 'antd';
import { createBrowserRouter, createHashRouter,RouterProvider } from "react-router-dom";
import zhCN from 'antd/es/locale/zh_CN';
import ErrorBoundary from "../components/ErrorBoundary";
import routes from './../routes/index';
import './../styles/index.scss';

const router = createHashRouter(routes);
const App = () => (
  <ConfigProvider locale={zhCN} theme={{
    components: {
    },
  }} >
    <ErrorBoundary>
      <RouterProvider
        router={router}
      />
    </ErrorBoundary>
  </ConfigProvider>
);

export default App;

