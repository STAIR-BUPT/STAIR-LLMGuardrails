import { post, get } from './../../utils/request.js';

// 注册
export const register = (data) => {
  // console.log("data", data)
  // 模拟注册
  // return new Promise((res, rej) => {
  //   res({ code: 0 })
  // })
  return post('/user/register/', data);
}

export const getUserInfo = () => {
  return get('/user/info');
}
