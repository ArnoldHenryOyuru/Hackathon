import { request } from "./client";
export const getLatestInsights = () => request("/api/insights/latest");
export const generateInsights = () => request("/api/insights/generate", { method:"POST" });
