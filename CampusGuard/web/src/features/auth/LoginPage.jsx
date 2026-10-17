import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Page from "../../components/Page";
import Button from "../../components/Button";
import Field from "../../components/Field";
import { login } from "../../api/auth";

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({username:"", password:""});
  const [error, setError] = useState("");
  const set = (key) => (event) => setForm({...form, [key]:event.target.value});
  async function submit(event) {
    event.preventDefault();
    try {
      const session = await login(form);
      localStorage.setItem("campusguard_session", JSON.stringify(session));
      navigate(session.role === "student" ? "/" : "/admin");
    } catch (submissionError) { setError(submissionError.message); }
  }
  return <Page eyebrow="Secure access" title="Sign in">
    <p className="pageIntro">Students can report anonymously. Staff access Dispatch, Insights, and Admin tools.</p>
    <form className="loginForm" onSubmit={submit}>
      <Field label="Username"><input value={form.username} onChange={set("username")} required /></Field>
      <Field label="Password"><input type="password" value={form.password} onChange={set("password")} required /></Field>
      {error && <p className="notice">{error}</p>}
      <Button className="buttonPrimary">SIGN IN</Button>
    </form>
    <p className="loginDemo mono">Demo: student/student123 · admin/admin123 · responder/responder123</p>
  </Page>;
}
