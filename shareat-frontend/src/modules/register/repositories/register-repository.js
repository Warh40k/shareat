import httpClient from '@/core/plugins/http-client';

const apiRoute = '/api/auth';

export async function Register(authData) {
  const result = await httpClient
    .post(`${apiRoute}/register`, authData)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка регистрации');
    });

  return result;
}
