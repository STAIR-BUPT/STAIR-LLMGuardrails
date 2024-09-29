import { post, get } from './../../utils/request.js';

// 登录
export const login = (data) => {
  // console.log("data", data)
  // 模拟登录
  // return new Promise((res, rej) => {
  //   if (data.password === '123456' && data.username === 'admin') {
  //     res({ code: 0, data: { username: 'admin', token: 'wertyujktyuiopghjkl', role: 'sysAdmin'} })
  //   } else {
  //     res({ code: -1, message: '用户名或密码错误！' })
  //   }
  // })
  return post('/user/login/', data);
}

export const getUserInfo = () => {
  return get('/user/info');
}
