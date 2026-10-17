import { useCallback } from "react";
import { getAlerts, updateStatus } from "../../api/alerts";
import { usePolling } from "../../hooks/usePolling";
import SosBanner from "./SosBanner";
import IncidentCard from "./IncidentCard";
export default function AlertList(){const load=useCallback(getAlerts,[]);const {value:alerts,error}=usePolling(load,4000);if(error)return <p className="notice">{error}</p>;if(!alerts)return <p className="mono">LOADING ALERTS...</p>;const sos=alerts.filter(a=>a.type==="sos"),reports=alerts.filter(a=>a.type==="report");const onStatus=(id,status)=>updateStatus(id,status);return <><section>{sos.map(a=><SosBanner key={a.id} alert={a} onStatus={onStatus}/>)}</section><section className="ledger"><div className="ledgerHead"><span>TIME</span><span>PRIORITY</span><span>INCIDENT / ACTION</span><span>STATUS</span></div>{reports.map(a=><IncidentCard key={a.id} alert={a} onStatus={onStatus}/> )}</section></>}
