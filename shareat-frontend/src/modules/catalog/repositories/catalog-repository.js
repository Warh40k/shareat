import axios from 'axios';

const apiRoute = '/api/catalog';

export async function GetAllProducts() {
  const url = `${apiRoute}/getProducts`;

  const result = await axios
    .get(url)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка получения списка продуктов');
    });

  return result;
}

export async function CreateProduct(formData) {
  const result = await axios
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
