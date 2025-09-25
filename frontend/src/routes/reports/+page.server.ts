import type { PageServerLoad } from "./$types";

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
