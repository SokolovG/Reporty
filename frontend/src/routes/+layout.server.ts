import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: LayoutServerLoad = async ({ cookies, url }) => {
  const authToken = cookies.get('authToken');

  const publicPaths = ['/login', '/register'];
  const isPublicPath = publicPaths.some(path => url.pathname.startsWith(path));

  if (!authToken && !isPublicPath) {
    throw redirect(302, '/login');
  }

  if (!authToken) {
    return { user: null };
  }

  if (isPublicPath && url.pathname === '/login') {
    throw redirect(302, '/');
  }

  return {
    user: null
  };
};
