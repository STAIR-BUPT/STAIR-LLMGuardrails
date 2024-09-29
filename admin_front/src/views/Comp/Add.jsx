import React, {useEffect} from 'react';
import { Button, Modal, Form, Input, Select, DatePicker, Row, Col, Space } from 'antd';

const layout = {
  labelCol: {
    span: 5,
  },
  wrapperCol: {
    span: 19,
  },
};
const tailLayout = {
  wrapperCol: {
    offset: 9,
    span: 15,
  },
};
const { Option } = Select;
const Add = (props = {}) => {
  const { open, editData = {}, onCancel = () => {}, onFinish = () => {} } = props;
  const [form] = Form.useForm();

  const onCancelFunc = () => {
    form.resetFields();
    onCancel();
  }
  const onFinishFunc = (values) => {
    console.log(values);
    onFinish({id: editData.id || null ,...values}, () => {
      onCancelFunc();
    })
  };

  useEffect(() => {
    if (editData.id) {
      form.setFieldsValue({
        ...editData,
      })
    } else {
      form.setFieldsValue({})
    }
  }, [editData.id])


  return (
    <Modal className="cases_modal" title={editData.id? "编辑组件" : "新增组件"} open={open} onCancel={onCancelFunc} footer={null}>
      <Form
        form={form}
        {...layout}
        onFinish={onFinishFunc}
      >
        <Row>
          <Col span={24}><Form.Item name="name" label="组件名称" rules={[{ required: true }]}>
            <Input placeholder="组件名称" />
          </Form.Item></Col>
          <Col span={24}><Form.Item name="initMethod" label="init方法" rules={[{ required: true }]}>
            <Input.TextArea rows={4} placeholder="您的init方法" />
          </Form.Item></Col>
          <Col span={24}><Form.Item name="validateMethod" label="validate方法" rules={[{ required: true }]}>
            <Input.TextArea rows={4} placeholder="您的validate方法" />
          </Form.Item></Col>
          <Col span={24}><Form.Item {...tailLayout}>
            <Space>
              <Button type="primary" htmlType="submit">
                提交
              </Button>
              <Button htmlType="button" onClick={onCancelFunc}>
                返回
              </Button>
            </Space>
          </Form.Item></Col>
        </Row>
      </Form>
    </Modal>
  )
}

export default Add;
