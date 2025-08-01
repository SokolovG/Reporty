import {redirect} from "@sveltejs/kit";
import type { PageServerLoad, Actions } from './$types';
import { BACKEND_API_URL } from '$env/static/private';

export const load: PageServerLoad = async ({ parent }) => {
  const { user } = await parent();

  if (user) {
    throw redirect(302, '/');
  }

  return {};
};

export const actions: Actions = {
    login: async ({ request }) => {
        const formData = await request.formData();
        const email = formData.get('email');
        const password = formData.get('password');

        if (!email || !password) {
            return { error: 'Email and password are required' };
        }

        try {
            const loginData = {
                email: email.toString(),
                password: password.toString()
            };

            const response = await fetch(`${BACKEND_API_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData)
            });

            if (!response.ok) {
                return { error: 'Invalid email or password' };
            }


        } catch (error) {
            return { error: 'Server connection error' };
        }

        throw redirect(303, '/');
    }
};
