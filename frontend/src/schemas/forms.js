export function validateTransaction(values) {
  // Browser validation improves feedback, but Flask repeats every rule for security.
  if (!values.categoryId || !values.date || Number(values.amount) <= 0) return 'Choose a category, date, and positive amount.'
  return ''
}
