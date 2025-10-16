
import type { PageServerLoad, Actions } from "./$types";

export const load: PageServerLoad = async ({ fetch }) => {

    try {
        const reportsResponse = await fetch('/api/v1/reports');
        if (!reportsResponse.ok) {
            return { reports: []};
        }

        const reports = await reportsResponse.json();
        return { reports };
    } catch (error) {
        // If it's a redirect, re-throw it
        if (error instanceof Response) {
            console.error(error)
            throw error;
        }
        return { reports: [] };
    }
};

export const actions: Actions = {

    create: async ({ request, fetch }) => {
        const formData = await request.formData()
        const data = formData.get("data")

        try {
            const body = {
                "data": data?.toString()
            };
            const response = await fetch("api/v1/reports", {
                method: "POST",
                body: JSON.stringify(body),
            });

            if (!response.ok) {
                return { error: 'Failed to create report' };
            }
        } catch (error) {

        }
    }

}
