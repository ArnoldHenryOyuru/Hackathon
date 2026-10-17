import { useState } from "react";
import Button from "../../components/Button";
import Field from "../../components/Field";
import Select from "../../components/Select";
import { createReport } from "../../api/reports";
const categories=["suspicious person","harassment","theft","unsafe area","broken lighting","vandalism","medical concern","other"];
const locations=["Hostel Gate","Library","Parking Lot A","Parking Lot B","Main Gate","Cafeteria","Science Block","Sports Field","Admin Block","Other"];
export default function ReportForm({ onSubmitted }) {
  const [form,setForm]=useState({category:"",description:"",location:"",anonymous:false}); const [busy,setBusy]=useState(false); const set=(key)=>(event)=>setForm({...form,[key]:event.target.type==="checkbox"?event.target.checked:event.target.value});
  async function submit(event){event.preventDefault();setBusy(true);try{const result=await createReport(form);onSubmitted(result)}catch(error){onSubmitted(null,error.message)}finally{setBusy(false)}}
  return <form onSubmit={submit}><Select label="Category" value={form.category} onChange={set("category")} options={categories}/><Field label="Description"><textarea value={form.description} onChange={set("description")} placeholder="What happened?" required /></Field><Select label="Campus location" value={form.location} onChange={set("location")} options={locations}/><Field label={<span className="checkbox"><input type="checkbox" checked={form.anonymous} onChange={set("anonymous")}/> Report anonymously</span>}><span /></Field><Button className="buttonPrimary" disabled={busy}>{busy?"SAVING":"SUBMIT REPORT"}</Button></form>;
}
