import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ fetch, params }) => {
    const { id } = params;

    try {
        const response = await fetch(`/api/v1/reports/${id}`);

        if (!response.ok) {
            if (response.status === 404) {
                throw error(404, "Report not found");
            }
            throw error(response.status, "Failed to load report");
        }

        const result = await response.json();

        if (result.success && result.data) {
            return {
                report: result.data
            };
        } else {
            throw error(500, "Invalid response format from API");
        }
    } catch (err) {
        console.error("Error loading report:", err);
        if (err && typeof err === 'object' && 'status' in err) {
            throw err;
        }
        throw error(500, "Internal error loading report");
    }
};
