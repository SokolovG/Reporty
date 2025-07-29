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

  // Validate token by making a simple request to backend
  // Change to api me endpoint
  try {
    const response = await fetch(`${BACKEND_API_URL}/v1/records`, {
      headers: { 'Authorization': authToken }
    });

    if (response.status === 401) {
      // Token is invalid, clear it and redirect to login
      cookies.delete('authToken', { path: '/' });
      throw redirect(302, '/login');
    }
  } catch (error) {
    // If there's a network error, don't redirect - let the page handle it
    console.log('Token validation failed:', error);
  }

  return {
    user: null
  };
};
