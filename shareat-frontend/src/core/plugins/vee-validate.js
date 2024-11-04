import Vue from 'vue';
import { extend, ValidationProvider, ValidationObserver } from 'vee-validate';
import { required, email, confirmed, length, max } from 'vee-validate/dist/rules';

extend('required', {
  ...required,
  message: 'Обязательное поле',
});

extend('email', {
  ...email,
  message: 'Введите корректную почту',
});

extend('confirmed', {
  ...confirmed,
  message: 'Значение должно совпадать',
});

extend('max', {
  ...max,
  message: `Длина поля не должна быть больше {length} символов`,
});

extend('length', {
  ...length,
  message: `Длина поля должна быть {length} символов`,
});

extend('date_more', {
  validate: (value, { date }) => {
    if (!date || !value) {
      return true;
    }

    const date1 = new Date(value);
    const date2 = new Date(date);

    return date1 > date2 || `Дата должна быть больше: ${date2.toLocaleString()}`;
  },
  params: ['date'],
});

Vue.component('ValidationProvider', ValidationProvider);
Vue.component('ValidationObserver', ValidationObserver);
