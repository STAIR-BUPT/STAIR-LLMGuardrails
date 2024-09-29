import mjFetch, { MjFetchApi } from 'mj-fetch';
import { apiPrefix } from './host';

const ENV = process.env.NODE_ENV || 'development';

export const getToken = async () => {
  const token = localStorage.getItem("token");
  if (token) myFetch.setConfig({headers: { Authorization: `Bearer ${token}` }})
};

export const myFetch = new MjFetchApi({
  timeout: '6000', // 设置统一超时
  before: (v) => ({...v, url: v.url.includes('http') ? v.url:`${apiPrefix[ENV]}${v.url}`}),
  after: () => {},  // 请求后置回调，如关闭loading效果
  withCredentials: false, // 后端将Access-Control-Allow-Origin设为*后，这边需设置为false
  credentials: false, // 发送凭证方式
  middlewares: [(rst) => {
    if ([20001, 20002].indexOf(rst.code) > -1) {
      console.log("登录失效，重新授权");
      localStorage.removeItem("token");
      localStorage.removeItem("name");
      localStorage.removeItem("username");
      window.location.href="/#/login";
    }
    return rst;
  }]
});
(async () => await getToken())();

export const get = (url, data, opts) => myFetch.get(url, data, opts).catch((err) => console.log(err));
export const post = (url, data, opts) => myFetch.post(url, data, opts).catch((err) => console.log(err));
