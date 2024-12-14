import httpClient from '@/core/plugins/http-client';

const apiRoute = '/api/catalog';

export async function GetAllProducts() {
  const url = `${apiRoute}/getProducts`;

  const result = await httpClient
    .get(url)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка получения списка продуктов');
    });

  return result;
}

export async function CreateProduct(formData) {
  const result = await httpClient
    .post(`${apiRoute}/createProduct`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка создания продукта');
    });

  return result;
}

export async function DeleteProduct(id) {
  const result = await httpClient
    .delete(`${apiRoute}/deleteProduct/${id}`)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка удаления продукта');
    });

  return result;
}

export async function UpdateProduct(id, formData) {
  const result = await httpClient
    .put(`${apiRoute}/updateProduct/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка изменения продукта');
    });

  return result;
}
