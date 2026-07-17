export function Status({ children, type = 'info' }) {
  return <p className={`status ${type}`} role={type === 'error' ? 'alert' : 'status'}>{children}</p>
}

export function EmptyState({ children }) {
  return <p className="empty">{children}</p>
}
