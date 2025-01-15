import httpClient from '@/core/plugins/http-client';

const apiRoute = '/api/report';

export async function CreateReport(data) {
  const url = `${apiRoute}/createReport`;

  const result = await httpClient
    .post(url, data)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка заказа отчета');
    });

  return result;
}

