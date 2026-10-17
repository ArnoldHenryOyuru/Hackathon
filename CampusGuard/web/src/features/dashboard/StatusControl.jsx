import Button from "../../components/Button";
export default function StatusControl({ value, onChange }) { return <div className="statusControl">{["New","Investigating","Resolved"].map(status=><Button key={status} className={value===status?"buttonPrimary":""} onClick={()=>onChange(status)}>{status}</Button>)}</div>; }
