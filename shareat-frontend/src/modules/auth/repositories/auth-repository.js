import axios from 'axios';

const apiRoute = '/api/auth';

export async function Login(login, password) {
  const data = new URLSearchParams({
    grant_type: 'password',
    username: login,
    password,
    client_id: '',
    client_secret: '',
  });

  const url = `${apiRoute}/login`;

  axios({
    method: 'post',
    url: url,
    data: data.toString(),
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
  })
  .then(response => {
    return response.data;
  })
  .catch(error => {
    throw new Error(error?.response?.data?.message || 'Ошибка авторизации');
  });
}

export async function Logout() {
  const url = `${apiRoute}/logout`;

  const result = await axios
    .post(url, null)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка выхода');
    });

  return result;
}
