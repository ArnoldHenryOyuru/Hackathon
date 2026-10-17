import { useCallback, useState } from "react";
export function useGeolocation() {
  const [position, setPosition] = useState({ lat:null, lng:null });
  const capture = useCallback(() => new Promise((resolve) => { if (!navigator.geolocation) return resolve(position); navigator.geolocation.getCurrentPosition((p) => { const next={lat:p.coords.latitude,lng:p.coords.longitude}; setPosition(next); resolve(next); }, () => resolve(position), { timeout:3000 }); }), [position]);
  return { position, capture };
}
