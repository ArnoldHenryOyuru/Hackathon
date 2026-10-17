import Page from "../../components/Page";
import AlertList from "./AlertList";
import { getHealth } from "../../api/health";
import { usePolling } from "../../hooks/usePolling";
export default function DashboardPage(){const {value:health}=usePolling(getHealth,10000);return <Page eyebrow="Campus security · live dispatch" title="Incident ledger"><p className="pageIntro">Alerts refresh every 4 seconds. SOS events stay at the top. <span className={`aiStatus aiStatus-${health?.ai||"unknown"}`}>AI: {health?.ai||"checking"}</span></p><AlertList/></Page>}
