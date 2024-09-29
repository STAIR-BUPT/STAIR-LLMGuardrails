import { post, get } from './../../utils/request.js';

export const getList = (data) => {
  return post('/user/components/list/', data);
}
export const updateList = (data) => {
  return post('/user/components/update/', data);
}
export const addList = (data) => {
  return post('/user/components/add/', data);
}
export const delList = (data) => {
  return get('/user/components/del/', data);
}
