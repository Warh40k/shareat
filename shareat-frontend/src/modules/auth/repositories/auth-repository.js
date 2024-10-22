import axios from 'axios';

const apiRoute = '/api/auth';

export async function Login(login, password) {
  const data = {
    login,
    password,
  };

  // TODO: уточнить роут
  const url = `${apiRoute}/userAuth`;

  // const result = await axios
  //   .post(url, data)
  //   .then((response) => response.data)
  //   .catch((error) => {
  //     throw new Error(error?.response?.data?.message || 'Ошибка авторизации');
  //   });

  // return result;
  return true;
}

export async function Logout() {
  // TODO: уточнить роут
  const url = `${apiRoute}/logout`;

  // const result = await axios
  //   .post(url, null)
  //   .then((response) => response.data)
  //   .catch((error) => {
  //     throw new Error(error?.response?.data?.message || 'Ошибка выхода');
  //   });

  // return result;
  return true;
}
