import { useState } from "react";
import Button from "../../components/Button";
import { sendSos } from "../../api/sos";
import { useGeolocation } from "../../hooks/useGeolocation";

const GPS_WAIT_MS = 2500;
const NO_POSITION = { lat: null, lng: null };

export default function SosButton({ onSent }) {
  const [busy, setBusy] = useState(false);
  const { capture } = useGeolocation();

  async function handleClick() {
    if (busy) return;
    setBusy(true);
    try {
      // SOS must never wait on the location prompt: after a short wait, send without GPS.
      const position = await Promise.race([
        capture(),
        new Promise((resolve) => setTimeout(() => resolve(NO_POSITION), GPS_WAIT_MS)),
      ]);
      const result = await sendSos({ ...position, timestamp: new Date().toISOString() });
      onSent(result);
    } catch (error) {
      onSent(null, error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Button
      className={`buttonEmergency sosButton${busy ? " sosBusy" : ""}`}
      onClick={handleClick}
      disabled={busy}
      aria-busy={busy}
    >
      {busy ? "SENDING" : "SOS"}
    </Button>
  );
}
