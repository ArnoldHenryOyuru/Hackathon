export async function request(path, options = {}) {
  let session = null;
  try { session = JSON.parse(localStorage.getItem("campusguard_session") || "null"); } catch {}
  const auth = session?.token ? { Authorization: `Bearer ${session.token}` } : {};
  const response = await fetch(path, { headers: { "Content-Type": "application/json", ...auth, ...options.headers }, ...options });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || "Request failed.");
  return data;
}
