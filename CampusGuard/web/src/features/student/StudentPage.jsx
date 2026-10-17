import { useState } from "react";
import Page from "../../components/Page";
import SosButton from "./SosButton";
import ReportForm from "./ReportForm";
import ConfirmationScreen from "./ConfirmationScreen";
import Button from "../../components/Button";
import "./student.css";
export default function StudentPage(){const [mode,setMode]=useState("home");const [result,setResult]=useState(null);const [sosResult,setSosResult]=useState(null);const [notice,setNotice]=useState("");
 return <Page eyebrow="Student safety" title={null}><div className="student"><SosButton onSent={(data,error)=>{if(error){setNotice(error);setTimeout(()=>setNotice(""),5000)}else{setSosResult(data);setMode("sosConfirmation")}}}/><p className="sosHint">Immediate alert · GPS if permitted · no login</p>{notice&&<div className="notice fadeIn">{notice}</div>}{mode==="home"&&<Button className="reportButton" onClick={()=>setMode("report")}>REPORT A DANGER</Button>}{mode==="report"&&<section className="report"><div className="eyebrow">New incident</div><h2>Report a danger</h2><ReportForm onSubmitted={(data,error)=>{if(error)setNotice(error);else{setResult(data);setMode("confirmation")}}}/></section>}{mode==="confirmation"&&<ConfirmationScreen result={result} onAgain={()=>setMode("home")}/>} {mode==="sosConfirmation"&&<ConfirmationScreen isSos result={sosResult} onAgain={()=>setMode("home")}/>}</div></Page>}
