import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import { EmptyState, Status } from '../../components/shared/Status'
import { currentMonth, formatMoney } from '../../utils/format'
import { useProductContext } from '../../context/UseProductContext'

export function BudgetsPage() {
  const [month, setMonth] = useState(currentMonth()); const [budgets, setBudgets] = useState([]); const [categories, setCategories] = useState([]); const [categoryId, setCategoryId] = useState(''); const [amount, setAmount] = useState(''); const [message, setMessage] = useState(''); const { user } = useProductContext()
  const load = () => { api.get(`/budgets?month=${month}`).then((data) => setBudgets(data.budgets)).catch((p) => setMessage(p.error)); api.get('/categories').then((data) => setCategories(data.categories.filter((item) => item.type === 'expense'))) }
  useEffect(load, [month])
  async function submit(event) { event.preventDefault(); try { await api.put('/budgets', { month, categoryId: Number(categoryId), amountMinor: Math.round(Number(amount) * 100) }); setAmount(''); load() } catch (problem) { setMessage(problem.error) } }
  return <><header><h2>Budgets</h2><input type="month" value={month} onChange={(e) => setMonth(e.target.value)} /></header><form className="inline-form" onSubmit={submit}><select required value={categoryId} onChange={(e) => setCategoryId(e.target.value)}><option value="">Expense category</option>{categories.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select><input required min="0.01" step="0.01" type="number" placeholder="Budget amount" value={amount} onChange={(e) => setAmount(e.target.value)} /><button>Save budget</button></form>{message && <Status type="error">{message}</Status>}{budgets.length ? <ul className="records">{budgets.map((budget) => <li key={budget.id}><span>{budget.category.name} <small>{budget.status.replace('_', ' ')}</small></span><strong>{formatMoney(budget.spentMinor, user.defaultCurrency)} / {formatMoney(budget.amountMinor, user.defaultCurrency)}</strong><small>{formatMoney(budget.remainingMinor, user.defaultCurrency)} remaining</small></li>)}</ul> : <EmptyState>No budgets for this month.</EmptyState>}</>
}
