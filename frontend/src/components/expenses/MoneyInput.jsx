export function MoneyInput({ value, onChange, label = 'Amount' }) {
  // The component accepts a readable decimal; the API boundary converts it to minor units.
  return <label>{label}<input required min="0.01" step="0.01" type="number" value={value} onChange={onChange} /></label>
}
