import type { LayoutServerLoad } from './$types';
import { redirect } from '@sveltejs/kit';
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
  const accessToken = cookies.get("accessToken")

  async function tokenRefresh() {
    try {
      const refreshResponse = await fetch('/api/v1/auth/refresh', {
        method: 'POST',
        credentials: 'include'
      });
      return refreshResponse.ok;
      } catch {
        return false;
      }
    }

  if (!accessToken) {
    if (!isPublicPath) {
      throw redirect(302, '/login?error=no_token');
    }
    return { user: null };
  }

  try {
    const publicKey = await getPublicKey();
    const { payload } = await jwtVerify(accessToken, publicKey);


    if (payload.exp && payload.exp < Date.now() / 1000) {
      const refreshed = await tokenRefresh();
      if (!refreshed) {
        if (!isPublicPath) {
          throw redirect(302, '/login?error=token_expired');
        }
        return { user: null };
      }
    }

  const newAccessToken = cookies.get("accessToken");
  if (newAccessToken) {
    const { payload } = await jwtVerify(newAccessToken, publicKey)
    return {user: {id: payload.id}}
  }

  return {
      user: {
        id: payload.sub,
      }
    };

    } catch (error) {
    if (!isPublicPath) {
      throw redirect(302, '/login?error=invalid_token');
    }
    return { user: null };
  }
};
