import { useEffect, useState } from 'react'
import { api } from '../../api/client'
import { EmptyState, Status } from '../../components/shared/Status'

export function CategoriesPage() {
  const [categories, setCategories] = useState([]); const [name, setName] = useState(''); const [type, setType] = useState('expense'); const [message, setMessage] = useState('')
  const load = () => api.get('/categories?includeArchived=true').then((data) => setCategories(data.categories)).catch((p) => setMessage(p.error))
  useEffect(load, [])
  async function submit(event) { event.preventDefault(); try { await api.post('/categories', { name, type }); setName(''); load() } catch (problem) { setMessage(problem.error) } }
  return <><h2>Categories</h2><form className="inline-form" onSubmit={submit}><input required placeholder="Category name" value={name} onChange={(e) => setName(e.target.value)} /><select value={type} onChange={(e) => setType(e.target.value)}><option value="expense">Expense</option><option value="income">Income</option></select><button>Add category</button></form>{message && <Status type="error">{message}</Status>}{categories.length ? <ul className="records">{categories.map((category) => <li key={category.id}><span>{category.name} <small>({category.type})</small></span><button onClick={async () => { await api.patch(`/categories/${category.id}`, { isActive: !category.isActive }); load() }}>{category.isActive ? 'Archive' : 'Restore'}</button></li>)}</ul> : <EmptyState>Create income and expense categories first.</EmptyState>}</>
}
