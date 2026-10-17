import StatusControl from "./StatusControl";

function formatElapsedTime(createdAt) {
  const elapsedMinutes = Math.max(0, Math.floor((Date.now() - new Date(createdAt)) / 60000));
  if (elapsedMinutes < 60) {
    return `${elapsedMinutes} min ago`;
  }

  return `${Math.floor(elapsedMinutes / 60)} hr ago`;
}

export default function SosBanner({ alert, onStatus }) { return <article className="sosBanner fadeIn"><div><span className="eyebrow">SOS ALERT · {formatElapsedTime(alert.created_at)}</span><strong>{alert.lat!=null?`${alert.lat.toFixed(5)}, ${alert.lng.toFixed(5)}`:"Location unavailable"}</strong><small className="mono">{new Date(alert.created_at).toLocaleString()}</small></div><StatusControl value={alert.status} onChange={(status)=>onStatus(alert.id,status)}/></article>; }
