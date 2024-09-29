import React, { useEffect, useState, useMemo} from "react";
import { Space, Form, Input, Button, Affix, message } from "antd";
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Link, useNavigate } from "react-router-dom";
import {getUserInfo, login} from "./service";
import {myFetch} from "../../utils/request";

const colProps = {
  xs: { span: 10},
  lg: { span: 10}
};
const { Item } = Form;
const LoginPage = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    const rst = await login(values) || {};
    if (rst.status === "success") {
      message.success("登录成功");
      localStorage.setItem("username", values.username);
      localStorage.setItem("token", rst.data);
      // localStorage.setItem("role", rst.data.role);
      if (rst.data) myFetch.setConfig({headers: { Authorization: `Bearer ${rst.data}` }})
      const urlParams = new URL(window.location.href).searchParams;
      navigate(urlParams.get('redirect') || '/');
    } else {
      message.error(rst.msg)
    }
  };

  return <div className={`admin_login theme_one`}>
    <div className="container">
      <div {...colProps} className="container_form" >
        <Form form={form} onFinish={onFinish}>
          <div className="head-title">欢迎登录</div>
          <Item name="username"
            rules={[{required: true, message: 'Please input your Username!'}]}>
            <Input size="large" prefix={<UserOutlined />} placeholder="请输入用户名" />
          </Item>
          <Item name="password"
            rules={[{required: true, message: 'Please input your Password!'}]}>
            <Input.Password size="large" prefix={<LockOutlined />} type="password" placeholder="请输入密码" />
          </Item>
          <Item>
            <Button block size="large" type="primary" htmlType="submit">登录</Button>
            {/*Or <a href="/">返回首页!</a>*/}
            <div style={{marginTop: '10px'}}>
              <span>还没有账号？</span>
              <a href="/#/register">去注册</a>
            </div>
          </Item>
        </Form>
      </div>
    </div>
  </div>
};

export default LoginPage;
