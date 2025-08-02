import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: LayoutServerLoad = async ({ url, fetch }) => {

  const publicPaths = ['/login', '/register'];
  const isPublicPath = publicPaths.some(path => url.pathname.startsWith(path));


  if (isPublicPath) {
        return {user: null};
  }

try {
    const response = await fetch('/api/v1/users/me');

    if (response.status === 401) {
      throw redirect(302, '/login?error=session_expired');
    }

    if (response.ok) {
      const user = await response.json();
      return { user };
    }
  } catch (error) {
    if (!(error instanceof Response)) {
      throw redirect(302, '/login?error=connection_error');
    }
    throw error;
  }
};
