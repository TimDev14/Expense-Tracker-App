export function formatMoney(amountMinor = 0, currency = 'USD') {
  return new Intl.NumberFormat(undefined, { style: 'currency', currency }).format(amountMinor / 100)
}

export function currentMonth() {
  return new Date().toISOString().slice(0, 7)
}
