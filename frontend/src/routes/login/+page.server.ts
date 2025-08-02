import {redirect} from "@sveltejs/kit";
import type { PageServerLoad, Actions } from './$types';

export const load: PageServerLoad = async ({ parent }) => {
  const { user } = await parent();

  if (user) {
    throw redirect(302, '/');
  }

  return {};
};

export const actions: Actions = {
    login: async ({ request, fetch }) => {
        const formData = await request.formData();
        const username = formData.get('username');
        const password = formData.get('password');

        if (!username || !password) {
            return { error: 'Username and password are required' };
        }

        try {
            const loginData = {
                username: username.toString(),
                password: password.toString()
            };

            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData),
                credentials: 'include'
            });

            if (!response.ok) {
                return { error: 'Invalid username or password' };
            }


        } catch (error) {
            console.log(error)
            return { error: 'Server connection error' };
        }

        throw redirect(303, '/');
    }
};
