import React, {useEffect, useState} from 'react';
import {Button, message, Popconfirm, Space, Table} from "antd";
import dayjs from "dayjs";
import Add from "./Add";
import {addList, getList, updateList, delList} from "./service";

const Comp = () => {
  const [data, setData] = useState([]);
  const [open, setOpen] = useState(false);
  const [editData, setEditData] = useState({});

  const fetchData = async () => {
    const rst = await getList() || {};
    if (rst.status === 'success') {
      setData(rst.data);
    }
  }

  useEffect(() => {
    fetchData();
  }, [])

  const addProps = {
    open,
    editData,
    onCancel: () => {
      setEditData({});
      setOpen(false)
    },
    onFinish: async (params) => {
      const rst = params.id ? await updateList(params) :  await addList(params) || {};
      if (rst.status === "success") {
        message.success('操作成功')
        fetchData();
        setOpen(false);
      } else {
        message.error(rst.message)
      }
    }
  }

  const columns = [
    {
      title: '组件名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'init 方法',
      dataIndex: 'initMethod',
      key: 'initMethod',
    },
    {
      title: 'validate 方法',
      dataIndex: 'validateMethod',
      key: 'validateMethod',
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
        {/*<a*/}
        {/*  key="edit"*/}
        {/*  onClick={() => {*/}
        {/*    setEditData(record);*/}
        {/*    setOpen(true);*/}
        {/*  }}>*/}
        {/*  编辑*/}
        {/*</a>*/}
        <Popconfirm
          title="删除"
          description="确认删除该条记录?"
          onConfirm={() => {
            delList({id}).then((res) => {
              if (res.status === "success") {
                message.success("删除成功");
                fetchData();
              }
            })
          }}
        >
          <a>删除</a>
        </Popconfirm>
      </Space>
    },
  ];

  return <div className="comp" style={{margin: '10px'}}>
    <Button onClick={() => setOpen(true)} style={{float: 'right', marginBottom: '10px'}} type="primary">新增</Button>
    <Table dataSource={data} columns={columns} />
    <Add {...addProps} />
  </div>
}

export default Comp;
