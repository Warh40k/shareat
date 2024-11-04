import httpClient from '@/core/plugins/http-client';

const apiRoute = '/api/admin'; //TODO: уточнить

//TODO: все урлы согласовать с бэком
export async function GetAllUsers() {
  const url = `${apiRoute}/getAll`;

  const result = await httpClient
    .get(url)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка получения списка пользователей');
    });

  return result;
}

export async function GetUserById(id) {
  const result = await httpClient
    .get(`${apiRoute}/getById/${id}`)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка получения данных пользователя');
    });

  return result;
}

export async function CreateUser(userCreateModel) {
  const result = await httpClient
    .post(`${apiRoute}/create`, userCreateModel)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка создания пользователя');
    });

  return result;
}

export async function UpdateUser(userUpdateModel) {
  const result = await httpClient
    .put(`${apiRoute}/update`, userUpdateModel)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка изменения пользователя');
    });

  return result;
}

export async function DeleteUser(id) {
  const result = await httpClient
    .delete(`${apiRoute}/delete/${id}`)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка удаления пользователя');
    });

  return result;
}

export async function ChangePassword(userUpdateModel) {
  const result = await httpClient
    .put(`${apiRoute}/changePassword`, userUpdateModel)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка изменения пароля пользователя');
    });

  return result;
}

export async function ChangePasswordProfile(userUpdateModel) {
  const result = await httpClient
    .put(`${apiRoute}/changePasswordProfile`, userUpdateModel)
    .then((response) => response.data)
    .catch((error) => {
      throw new Error(error?.response?.data?.message || 'Ошибка изменения пароля пользователя');
    });

  return result;
}
