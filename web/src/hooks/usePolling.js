import { useEffect, useState } from "react";
export function usePolling(loader, interval = 4000) {
  const [value, setValue] = useState(null); const [error, setError] = useState("");
  useEffect(() => { let active = true; const load = () => loader().then((data) => active && setValue(data)).catch((e) => active && setError(e.message)); load(); const timer = setInterval(load, interval); return () => { active=false; clearInterval(timer); }; }, [loader, interval]);
  return { value, error };
}
