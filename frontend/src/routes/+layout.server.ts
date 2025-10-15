import type { User } from '$lib/types/user';
import type { LayoutServerLoad } from './$types';
import { error, redirect } from '@sveltejs/kit';
import { jwtVerify, importSPKI } from 'jose';

const PUBLIC_KEY = `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6mvLrMaGO4ozU0mvCyUT
C/BiiG799gmg+DtXaTSzv5x2fv5kgA7ogp0wTR2KMHdChzXdrL/lXxzbd80dhxg6
AB9T77fIdz9a1dOEMNNXbLJvMu6ioUlN3sKmuqo2GMCMBR8Hm4r6/Jmz9d++xoRV
9cv8QyPIFNDkKKUf0H/pemXsIPp3XwIbG2q40nVHi7bCPjHbMsUAooalGmSkwLnv
ZpNNCC/Ee6NZ5x69K9H0a2zeE5VE9Ap638MIMO26NYWqjzkP1TC5mBbp94HON+MK
g5R0iGQuOLzPqxFK9YIDbWBb0U2qEQmzzEyuUJLJ+cYyPPsfgquIzbJyNIo4w0/M
7QIDAQAB
-----END PUBLIC KEY-----
`;

async function getPublicKey() {
  return await importSPKI(PUBLIC_KEY, 'RS256');
}

export const load: LayoutServerLoad = async ({ url, fetch, cookies }) => {
  const publicPaths = ['/login', '/register'];
  const isPublicPath = publicPaths.some(path => url.pathname.startsWith(path));
  const accessToken = cookies.get("accessToken");
  const refreshToken = cookies.get("refreshToken")


  async function tokenRefresh(): Promise<boolean> {
    try {
      const refreshResponse = await fetch('/api/v1/auth/refresh', {
        method: 'POST',
        credentials: 'include'
      });
      if (refreshResponse.ok) {
        return true;
      }
      return false;
    } catch (error) {
      console.error('Token refresh failed:', error);
      return false;
    }
  }

  async function fetchUser(): Promise<User> {
    const userResponse = await fetch("/api/v1/auth/me", {
      method: 'GET',
      credentials: 'include'
    });

    if (!userResponse.ok) {
      throw error(401, 'Failed to fetch user data');
    }

    const userData = await userResponse.json();

    if (!userData.success) {
      throw error(401, 'Failed to fetch user data');
    }

    return {
      id: userData.data.id,
      name: userData.data.name,
      email: userData.data.email,
      displayName: userData.data.displayName,
      department: userData.data.department,
      position: userData.data.position,
      aiAutoProcess: userData.data.aiAutoProcess,
      aiProviderId: userData.data.aiProviderId,
      isActive: userData.data.isActive,
      isVerify: userData.data.isActive,
      aiModelId: userData.data.aiModelId
    };
  }

  if (!accessToken) {
    if (refreshToken) {
      const refreshed = await tokenRefresh();
      if (refreshed) {
        const user = await fetchUser();
        return { user };
      }

    }
    if (!isPublicPath) {
      throw redirect(302, '/login?error=no_token');
    }
    return { user: null };
  }

  try {
    const publicKey = await getPublicKey();
    await jwtVerify(accessToken, publicKey);

    const user = await fetchUser();
    return { user };

  } catch (err) {
    console.error('Auth error:', err);

    if (err instanceof Error && err.name === 'JWTExpired') {
      const refreshed = await tokenRefresh();

      if (refreshed) {
        const user = await fetchUser();
        return { user };
      }
    }

    if (!isPublicPath) {
      throw redirect(302, '/login?error=invalid_token');
    }
    return { user: null };
  }

};
