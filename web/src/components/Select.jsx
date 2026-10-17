import Field from "./Field";
export default function Select({ label, value, onChange, options, required=true }) { return <Field label={label}><select value={value} onChange={onChange} required={required}><option value="">Select {label.toLowerCase()}</option>{options.map((option)=><option key={option} value={option}>{option}</option>)}</select></Field>; }
