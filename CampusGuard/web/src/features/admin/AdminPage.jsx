import { useCallback, useState } from "react";
import { Link } from "react-router-dom";
import Page from "../../components/Page";
import { addResponder, getAdminOverview, removeResponder } from "../../api/admin";
import { getHealth } from "../../api/health";
import { usePolling } from "../../hooks/usePolling";
import StatStrip from "../insights/StatStrip";

export default function AdminPage() {
  const [form, setForm] = useState({name:"", role:"", phone:"", email:"", notes:""});
  const [formError, setFormError] = useState("");
  const load = useCallback(async () => {
    const [overview, health] = await Promise.all([getAdminOverview(), getHealth()]);
    return { ...overview, health };
  }, []);
  const { value, error } = usePolling(load, 10000);
  function setField(key) { return (event) => setForm({...form, [key]:event.target.value}); }
  async function submitResponder(event) {
    event.preventDefault();
    setFormError("");
    try {
      await addResponder(form);
      setForm({name:"", role:"", phone:"", email:"", notes:""});
      window.location.reload();
    } catch (submissionError) {
      setFormError(submissionError.message);
    }
  }
  async function deleteResponder(id) {
    try { await removeResponder(id); window.location.reload(); }
    catch (removalError) { setFormError(removalError.message); }
  }
  if (error) return <Page eyebrow="Administration" title="Campus overview"><p className="notice">{error}</p></Page>;
  if (!value) return <Page eyebrow="Administration" title="Campus overview"><p className="mono">LOADING ADMIN OVERVIEW...</p></Page>;
  return <Page eyebrow="Administration" title="Campus overview">
    <p className="pageIntro">Operational summary and system health. <span className={`aiStatus aiStatus-${value.health.ai}`}>AI: {value.health.ai}</span></p>
    <StatStrip stats={value.stats} />
    <div className="eyebrow">Admin tools</div>
    <div className="adminActions">
      <Link className="button buttonPrimary" to="/dashboard">OPEN DISPATCH</Link>
      <Link className="button" to="/insights">OPEN INSIGHTS</Link>
    </div>
    <section className="adminResponders">
      <div className="eyebrow">Response network</div>
      <h2>People who can resolve issues</h2>
      <p className="pageIntro">Add trusted police, guardians, campus security, or medical responders for the team to contact.</p>
      <form className="responderForm" onSubmit={submitResponder}>
        <label>Name<input value={form.name} onChange={setField("name")} placeholder="Officer or guardian name" required /></label>
        <label>Role<select value={form.role} onChange={setField("role")} required><option value="">Select role</option><option>Police</option><option>Guardian</option><option>Campus security</option><option>Medical responder</option><option>Other</option></select></label>
        <label>Phone<input value={form.phone} onChange={setField("phone")} placeholder="+1 555 0100" required /></label>
        <label>Email<input type="email" value={form.email} onChange={setField("email")} placeholder="Optional" /></label>
        <label className="responderNotes">Notes<textarea value={form.notes} onChange={setField("notes")} placeholder="Area covered or availability" /></label>
        <button className="button buttonPrimary" type="submit">ADD RESPONDER</button>
      </form>
      {formError && <p className="notice">{formError}</p>}
      <div className="responderList">{value.responders.map((responder) => <article className="responder" key={responder.id}>
        <div><strong>{responder.name}</strong><span>{responder.role}</span></div>
        <a href={`tel:${responder.phone}`}>{responder.phone}</a>
        <span>{responder.email || "No email"}{responder.notes ? ` · ${responder.notes}` : ""}</span>
        <button className="button" type="button" onClick={() => deleteResponder(responder.id)}>REMOVE</button>
      </article>)}</div>
    </section>
    <section className="adminRecent">
      <div className="eyebrow">Latest activity</div>
      <h2>Recent alerts</h2>
      {value.recent_alerts.map((alert) => <article className="adminAlert" key={alert.id}>
        <span className="mono">#{alert.id} · {alert.type.toUpperCase()}</span>
        <strong>{alert.location || "Location unavailable"}</strong>
        <span>{alert.category || "SOS alert"} · {alert.priority} · {alert.status}</span>
        {alert.triage_pending ? <em>AI pending</em> : <small>{alert.triage_source}</small>}
      </article>)}
    </section>
  </Page>;
}
