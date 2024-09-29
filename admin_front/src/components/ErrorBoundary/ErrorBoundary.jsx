import React, { Component } from 'react';
import { Divider, Descriptions } from 'antd';

class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) { // 渲染备用UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) { // 打印错误信息
    this.setState({ error, errorInfo });
  }
  render () {
    if (this.state.hasError) {
      const { error = '', errorInfo = {} } = this.state;
      return (
        <div className="error_boundary">
          <Divider> <p className="error_boundary-tip">Sorry, something went Wrong. </p></Divider>
          <Descriptions title="错误详情" bordered column={1}>
            <Descriptions.Item label="错误原因"><code style={{color: '#f00'}}>{ error && error.toString() }</code></Descriptions.Item>
            <Descriptions.Item label="错误位置"><code>{ errorInfo.componentStack }</code></Descriptions.Item>
          </Descriptions>
        </div>
        
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
