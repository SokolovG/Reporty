import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
import { BACKEND_API_URL } from '$env/static/private';

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

try {
    const response = await fetch(`${BACKEND_API_URL}/me`, {
      headers: { 'Authorization': authToken }
    });

    if (response.status === 401) {
      cookies.delete('authToken', { path: '/' });
      throw redirect(302, '/login');
    }

    if (response.ok) {
      const user = await response.json();
      return { user };
    }
  } catch (error) {
    console.log('Token validation failed:', error);
  }
};
