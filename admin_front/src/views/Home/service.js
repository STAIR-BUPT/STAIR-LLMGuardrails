import { post, get } from './../../utils/request.js';

// 退出登录
export const loginOut = (data) => {
  // console.log("data", data)
  return post('/user/logout/', data);
}

export const getUserInfo = () => {
  return get('/user/info');
}

export const getTokenList = (data) => {
  return post('/user/token/list/', data);
}
export const updateTokenList = (data) => {
  return post('/user/token/update/', data);
}
export const addTokenList = (data) => {
  return post('/user/token/add/', data);
}
export const delTokenList = (data) => {
  return get('/user/token/del/', data);
}
