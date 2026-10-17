import Page from "../../components/Page";
import AlertList from "./AlertList";
export default function DashboardPage(){return <Page eyebrow="Campus security · live dispatch" title="Incident ledger"><p className="pageIntro">Alerts refresh every 4 seconds. SOS events stay at the top.</p><AlertList/></Page>}
