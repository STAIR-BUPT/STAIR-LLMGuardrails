import React, { useEffect, useState, useMemo} from "react";
import { Space, Form, Input, Button, Affix, message } from "antd";
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Link, useNavigate } from "react-router-dom";
import {register} from "./service";

const colProps = {
  xs: { span: 10},
  lg: { span: 10}
};
const { Item } = Form;
const RegisterPage = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    const rst = await register(values) || {};
    if (rst.status === "success") {
      message.success("用户注册成功,去登录！");
      // localStorage.setItem("token", rst.data.username);
      // localStorage.setItem("role", rst.data.role);
      // const urlParams = new URL(window.location.href).searchParams;
      navigate('/login');
    } else {
      message.error(rst.msg)
    }
  };

  return <div className={`admin_login theme_one`}>
    <div className="container">
      <div {...colProps} className="container_form" >
        <Form form={form} onFinish={onFinish}>
          <div className="head-title">欢迎注册</div>
          <Item name="username"
            rules={[{required: true, message: 'Please input your Username!'}]}>
            <Input size="large" prefix={<UserOutlined />} placeholder="请输入用户名" />
          </Item>
          <Item name="password"
            rules={[{required: true, message: 'Please input your Password!'}]}>
            <Input.Password size="large" prefix={<LockOutlined />} type="password" placeholder="请输入密码" />
          </Item>
          <Item name="confirmPassword"
                dependencies={['password']}
                rules={[
                  {required: true, message: 'Please confirm your Password !'},
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('password') === value) {
                        return Promise.resolve();
                      }
                      return Promise.reject(new Error('The new password that you entered do not match!'));
                    },
                  }),
                ]}>
            <Input.Password size="large" prefix={<LockOutlined />} type="password" placeholder="请确认密码" />
          </Item>
          <Item>
            <Button block size="large" type="primary" htmlType="submit">注册</Button>
            {/*Or <a href="/">返回首页!</a>*/}
            <div style={{marginTop: '10px'}}>
              <span>已有账号？</span>
              <a href="/#/login">去登录</a>
            </div>
          </Item>
        </Form>
      </div>
    </div>
  </div>
};

export default RegisterPage;
