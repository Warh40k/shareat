import httpClient from '@/core/plugins/http-client';

const apiRoute = '/api/Auth';

export async function Login(authData) {
  // const result = await httpClient
  //   .post(`${apiRoute}/Login`, authData)
  //   .then((response) => response.data)
  //   .catch((error) => {
  //     throw new Error(error?.response?.data?.message || 'Ошибка авторизации');
  //   });

  // return result;
  return true;
}

export async function Logout() {
  const result = await httpClient
    .post(`${apiRoute}/Logout`)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка выхода');
    });

  return result;
}
