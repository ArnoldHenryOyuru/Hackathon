import { request } from "./client";

export const login = (payload) => request("/api/auth/login", { method:"POST", body:JSON.stringify(payload) });
export async function logout() {
  try { await request("/api/auth/logout", { method:"POST" }); }
  finally { localStorage.removeItem("campusguard_session"); }
}
export function getSession() {
  try { return JSON.parse(localStorage.getItem("campusguard_session") || "null"); }
  catch { return null; }
}
