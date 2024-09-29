import React, {useEffect, useState} from 'react';
import {Menu, Dropdown, Table, Button, message, Space, Popconfirm, Modal} from 'antd';
import {
  ExclamationCircleFilled,
  HomeOutlined,
  Html5Outlined,
  IdcardOutlined,
  PlusCircleOutlined,
  UserOutlined
} from "@ant-design/icons";
import {Link, useNavigate} from 'react-router-dom';
import {addTokenList, delTokenList, getTokenList, loginOut, updateTokenList} from "./service";
import dayjs from 'dayjs';
import Comp from "../Comp";

const { confirm } = Modal;
const Home = () => {
  const [current, setCurrent] = useState('token');
  const [isLogin, setIsLogin] = useState(localStorage.getItem("token"));
  const username = localStorage.getItem("username");
  const navigate = useNavigate();
  const [data, setData] = useState([]);

  const fetchData = async () => {
    const rst = await getTokenList() || {};
    if (rst.status === 'success') {
      setData(rst.data);
    }
  }

  useEffect(() => {
    if (!isLogin) navigate('/login');
  }, [isLogin]);

  useEffect(() => {
    if (current === 'token') {
      fetchData();
    }
  }, [current])

  const items = [
    // {
    //   label: 'Mysite',
    //   key: 'site',
    //   icon: <Html5Outlined />,
    // },
    {
      label: '主页',
      key: 'home',
      icon: <HomeOutlined />,
    },
    {
      label: '身份验证',
      key: 'token',
      icon: <IdcardOutlined />,
    },
    {
      label: '组件上传/添加',
      key: 'comp',
      icon: <PlusCircleOutlined />,
    },
  ]

  const logOut = async () => {
    const rst = await loginOut() || {};
    if (rst.status === 'success') {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      setIsLogin(false);
    }
  }

  const renderTokenPage = () => {
    const columns = [
      {
        title: '姓名',
        dataIndex: 'username',
        key: 'username',
      },
      {
        title: 'token',
        dataIndex: 'token',
        key: 'token',
      },
      {
        title: '创建时间',
        dataIndex: 'createTime',
        key: 'createTime',
        render: (v) => (v && dayjs(v).format("YYYY-MM-DD HH:mm:ss"))
      },
      {
        title: "操作",
        dataIndex: 'id',
        valueType: 'option',
        hideInSearch: true,
        width: 100,
        render: (id, record) => <Space>
          <Popconfirm
            title="删除"
            description="确认删除该条记录?"
            onConfirm={() => {
              delTokenList({id}).then((res) => {
                if (res.status === "success") {
                  message.success("删除成功");
                  fetchData();
                  // actionRef.current?.reloadAndRest?.();
                }
              })
            }}
          >
            <a>删除</a>
          </Popconfirm>
        </Space>
      },
    ];
    return <div style={{margin: '10px'}}>
      <Button onClick={() => showConfirm()} style={{float: 'right', marginBottom: '10px'}} type="primary">新增</Button>
      <Table dataSource={data} columns={columns} />
    </div>
  }

  const showConfirm = () => {
    confirm({
      title: '确认新增一个Token?',
      icon: <ExclamationCircleFilled />,
      content: '',
      async onOk () {
        const rst = await addTokenList() || {};
        if (rst.status === 'success') {
          message.success("新增成功！")
          fetchData();
        }
      },
      onCancel() {
        console.log('Cancel');
      },
    });
  };

  return <div className="home_page">
    <Menu onClick={(e) => setCurrent(e.key)} selectedKeys={[current]} mode="horizontal" items={items} />
    {isLogin && <div className="header_r">
      <Dropdown
        menu={{
          items: [{  key: '1', label: (<div onClick={logOut}>退出登录</div>) }],
        }}
      >
        <a onClick={(e) => e.preventDefault()}>
          <UserOutlined style={{fontSize: '16px', marginRight: '5px'}} /><Link to="/">{username}</Link>
        </a>
      </Dropdown>

    </div>}
    {current === 'token' && renderTokenPage()}
    {current === 'comp' && <Comp />}
  </div>
}

export default Home;
