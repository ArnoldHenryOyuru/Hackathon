import { request } from "./client";
export const getAlerts = () => request("/api/alerts");
export const updateStatus = (id, status) => request(`/api/alerts/${id}/status`, { method:"PATCH", body:JSON.stringify({status}) });
