import {redirect} from "@sveltejs/kit";

export const actions = {
    default: async ({ request }) => {
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


        } catch (error) {
            console.log("Error:", error);
            return { error: 'Server connection error!' };
        }

        throw redirect(303, '/');
    }
};
