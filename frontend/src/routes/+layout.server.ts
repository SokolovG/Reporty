import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: LayoutServerLoad = async ({ url, fetch }) => {
  const publicPaths = ['/login', '/register'];
  const isPublicPath = publicPaths.some(path => url.pathname.startsWith(path));

  try {
    const response = await fetch('/api/v1/users/me');

    if (response.ok) {
      const user = await response.json();
      return { user };
    }

    if (response.status === 401) {
      if (isPublicPath) {
        return { user: null };
      } else {
        throw redirect(302, '/login?error=session_expired');
      }
    }

  } catch (error) {
    if (!(error instanceof Response)) {
      if (isPublicPath) {
        return { user: null };
      }
      throw redirect(302, '/login?error=connection_error');
    }
    throw error;
  }
};
