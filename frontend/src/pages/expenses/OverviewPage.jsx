import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import { EmptyState, Status } from '../../components/shared/Status'
import { currentMonth, formatMoney } from '../../utils/format'
import { useProductContext } from '../../context/UseProductContext'

export function OverviewPage() {
  const [month, setMonth] = useState(currentMonth())
  const [overview, setOverview] = useState(null)
  const [message, setMessage] = useState('')
  const { user } = useProductContext()
  useEffect(() => { api.get(`/reports/overview?month=${month}`).then((data) => setOverview(data.overview)).catch((problem) => setMessage(problem.error)) }, [month])
  return <><header><h2>Monthly overview</h2><label>Month <input type="month" value={month} onChange={(e) => setMonth(e.target.value)} /></label></header>{message && <Status type="error">{message}</Status>}{overview && <><div className="cards">{[['Income', overview.incomeMinor], ['Expenses', overview.expenseMinor], ['Balance', overview.balanceMinor]].map(([label, value]) => <article key={label}><p>{label}</p><strong>{formatMoney(value, user.defaultCurrency)}</strong></article>)}</div><h3>Recent transactions</h3>{overview.recentTransactions.length ? <ul className="records">{overview.recentTransactions.map((item) => <li key={item.id}><span>{item.description || item.category.name}</span><strong>{formatMoney(item.amountMinor, user.defaultCurrency)}</strong><small>{item.date}</small></li>)}</ul> : <EmptyState>No transactions for this month yet.</EmptyState>}</>}</>
}
