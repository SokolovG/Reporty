import { redirect } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ parent }) => {
  const { user } = await parent();

  // Если пользователь уже авторизован, редиректим на главную
  if (user) {
    throw redirect(302, '/');
  }

  return {};
};

export const actions: Actions = {
  register: async ({ request }) => {
    const formData = await request.formData();
    const email = formData.get('email');
    const password = formData.get('password');
    const confirmPassword = formData.get('confirmPassword');

    if (!email || !password || !confirmPassword) {
      return { error: 'All fields are required' };
    }

    if (password !== confirmPassword) {
      return { error: 'Passwords do not match' };
    }

    try {
      const registerData = {
        email: email.toString(),
        password: password.toString()
      };

      const response = await fetch('http://localhost:8080/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify(registerData)
      });

      if (!response.ok) {
        return { error: 'Registration failed' };
      }

      // Регистрация успешна - редиректим на логин
      throw redirect(302, '/login?message=Registration successful. Please log in.');
    } catch (error) {
      if (error instanceof Response) {
        throw error; // Это редирект
      }
      return { error: 'Server connection error' };
    }
  }
};
