import httpClient from '@/core/plugins/http-client';

const apiRoute = '/api/Auth';

export async function Register(authData) {
  const result = await httpClient
    .post(`${apiRoute}/Register`, authData)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка регистрации');
    });

  return result;
}
