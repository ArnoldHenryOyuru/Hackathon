import { useEffect, useState } from "react";
import Button from "../../components/Button";
import Page from "../../components/Page";
import { generateInsights, getLatestInsights } from "../../api/insights";
import StatStrip from "./StatStrip";
import BarChart from "./BarChart";
import Narrative from "./Narrative";
export default function InsightsPage(){const [data,setData]=useState(null);const [busy,setBusy]=useState(false);const [error,setError]=useState("");useEffect(()=>{getLatestInsights().then(setData).catch(()=>{})},[]);async function generate(){setBusy(true);setError("");try{setData(await generateInsights())}catch(e){setError(e.message)}finally{setBusy(false)}}return <Page eyebrow="Administrator view · weekly prevention" title="Prevention report" actions={<div className="reportAction"><Button className="buttonPrimary" onClick={generate} disabled={busy}>{busy?"GENERATING...":"GENERATE THIS WEEK'S REPORT"}</Button></div>}>{error&&<p className="notice">{error}</p>}{data?<><StatStrip stats={data.stats}/><Narrative text={data.narrative}/><div className="charts"><BarChart title="Incidents by category" rows={data.stats.by_category}/><BarChart title="Incidents by location" rows={data.stats.by_location} hotspot/><BarChart title="Incidents by hour" rows={data.stats.by_hour}/></div></>:<p className="mono">NO REPORT GENERATED. RUN THE WEEKLY REPORT.</p>}</Page>}
