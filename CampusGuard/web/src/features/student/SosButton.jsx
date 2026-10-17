import { useState } from "react";
import Button from "../../components/Button";
import { sendSos } from "../../api/sos";
import { useGeolocation } from "../../hooks/useGeolocation";

export default function SosButton({ onSent }) {
  const [busy, setBusy] = useState(false); const { capture } = useGeolocation();
  async function handleClick() { setBusy(true); try { const position = await capture(); await sendSos({ ...position, timestamp:new Date().toISOString() }); onSent(); } catch (error) { onSent(error.message); } finally { setBusy(false); } }
  return <Button className="buttonEmergency sosButton" onClick={handleClick} disabled={busy}>{busy ? "SENDING" : "SOS"}</Button>;
}
