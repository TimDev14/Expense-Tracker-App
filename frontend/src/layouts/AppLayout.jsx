import { NavLink, Outlet } from 'react-router-dom'
import { useProductContext } from '../context/UseProductContext'

const links = [['/', 'Overview'], ['/transactions', 'Transactions'], ['/categories', 'Categories'], ['/budgets', 'Budgets'], ['/reports', 'Reports'], ['/settings', 'Settings']]

export function AppLayout() {
  const { user, signOut } = useProductContext()
  return <main className="app-shell"><aside><h1>Ledgerly</h1><p>{user.displayName}</p><nav>{links.map(([to, label]) => <NavLink key={to} to={to} end={to === '/'}>{label}</NavLink>)}</nav><button onClick={signOut}>Sign out</button></aside><section className="content"><Outlet /></section></main>
}
