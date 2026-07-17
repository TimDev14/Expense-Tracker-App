import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import { EmptyState, Status } from '../../components/shared/Status'
import { currentMonth, formatMoney } from '../../utils/format'
import { useProductContext } from '../../context/UseProductContext'

export function ReportsPage() {
  const [month, setMonth] = useState(currentMonth()); const [categories, setCategories] = useState([]); const [message, setMessage] = useState(''); const { user } = useProductContext()
  useEffect(() => { api.get(`/reports/category-breakdown?month=${month}`).then((data) => setCategories(data.categories)).catch((p) => setMessage(p.error)) }, [month])
  return <><header><h2>Reports</h2><input type="month" value={month} onChange={(e) => setMonth(e.target.value)} /></header>{message && <Status type="error">{message}</Status>}{categories.length ? <ul className="records">{categories.map((category) => <li key={category.categoryId}><span>{category.name}</span><strong>{formatMoney(category.amountMinor, user.defaultCurrency)}</strong></li>)}</ul> : <EmptyState>No spending data for this month.</EmptyState>}</>
}
