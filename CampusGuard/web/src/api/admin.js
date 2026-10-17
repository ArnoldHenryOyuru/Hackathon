import { request } from "./client";
export const getAdminOverview = () => request("/api/admin/overview");
export const addResponder = (payload) => request("/api/admin/responders", { method:"POST", body:JSON.stringify(payload) });
export const removeResponder = (id) => request(`/api/admin/responders/${id}`, { method:"DELETE" });
