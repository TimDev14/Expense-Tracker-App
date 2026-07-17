import { useState } from 'react'
import { api } from '../../api/client'
import { Status } from '../../components/shared/Status'
import { useProductContext } from '../../context/UseProductContext'

export function SettingsPage() {
  const { user, updateUser } = useProductContext(); const [values, setValues] = useState(user); const [message, setMessage] = useState('')
  async function submit(event) { event.preventDefault(); try { const response = await api.patch('/profile', values); updateUser(response.user); setMessage('Saved.') } catch (problem) { setMessage(problem.error) } }
  return <><h2>Settings</h2><form onSubmit={submit}><label>Display name<input value={values.displayName} onChange={(e) => setValues({ ...values, displayName: e.target.value })} /></label><label>Currency<input maxLength="3" value={values.defaultCurrency} onChange={(e) => setValues({ ...values, defaultCurrency: e.target.value.toUpperCase() })} /></label><label>Timezone<input value={values.timezone} onChange={(e) => setValues({ ...values, timezone: e.target.value })} /></label><button>Save settings</button></form>{message && <Status>{message}</Status>}</>
}
