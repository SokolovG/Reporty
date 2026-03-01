
import { redirect } from "@sveltejs/kit";
import type { PageServerLoad, Actions } from "./$types";

export const load: PageServerLoad = async ({ fetch }) => {

    try {
        const reportsResponse = await fetch('/api/v1/reports');
        if (!reportsResponse.ok) {
            return { reports: [] };
        }

        const reports = await reportsResponse.json();
        return { reports };
    } catch (error) {
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
                "date": data?.toString()
            };
            const response = await fetch("/api/v1/reports", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify(body),
            });

            if (!response.ok) {
                return { error: 'Failed to create report' };
            }
        } catch (error) {
            console.error("Report creation error:", error);
        }
        throw redirect(303, "/reports");
    }


}
