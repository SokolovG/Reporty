import {redirect} from "@sveltejs/kit";

export const actions = {
    default: async ({ request, cookies }) => {
        const formData = await request.formData();
        const email = formData.get('email');
        const password = formData.get('password');

        try {
            const response = await fetch('http://localhost:8080/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json'},
                body: JSON.stringify({ email, password })
            });

            if (!response.ok) {
                return { error: 'Invalid email or password!' };
            }
            const access_token = response.headers.get("authorization");

            if (access_token) {
                cookies.set('authToken', access_token, {
                    path: '/',
                    httpOnly: true,
                    secure: false,
                    sameSite: 'strict',
                    maxAge: 60 * 60 * 24 * 7
                });
            } else {
                return { error: 'No token received' };
            }


        } catch (error) {
            console.log("Error:", error);
            return { error: 'Server connection error!' };
        }

        throw redirect(303, '/');
    }
};
