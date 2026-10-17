import { request } from "./client";
export const sendSos = (payload) => request("/api/sos", { method:"POST", body:JSON.stringify(payload) });
export const cancelSos = (id) => request(`/api/sos/${id}/cancel`, { method:"POST" });
