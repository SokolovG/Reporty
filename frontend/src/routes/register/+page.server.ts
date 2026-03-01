import { fail, redirect } from '@sveltejs/kit';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request, fetch }) => {
    const data = await request.formData();
    const email = data.get('email');
    const password = data.get('password');
    const name = data.get('name');

    if (!email || !password || !name) {
      return fail(400, { error: 'All fields are required' });
    }

    try {
      const response = await fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password, name })
      });

      const result = await response.json();

      if (!response.ok) {
        return fail(response.status, {
          error: result.message || 'Registration failed'
        });
      }

      throw redirect(303, '/login?registered=true');
    } catch (err) {
      if (err instanceof Response || (err && typeof err === 'object' && 'status' in err && 'location' in err)) {
        throw err;
      }
      console.error('Registration error:', err);
      return fail(500, { error: 'An unexpected error occurred during registration' });
    }
  }
};
