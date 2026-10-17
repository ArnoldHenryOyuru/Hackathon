import { request } from "./client";
export const createReport = (payload) => request("/api/reports", { method:"POST", body:JSON.stringify(payload) });
