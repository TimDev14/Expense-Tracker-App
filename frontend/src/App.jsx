import { Navigate, Route, Routes } from 'react-router-dom'
import { AuthPage } from './pages/auth/AuthPage'
import { BudgetsPage } from './pages/expenses/BudgetsPage'
import { CategoriesPage } from './pages/expenses/CategoriesPage'
import { OverviewPage } from './pages/expenses/OverviewPage'
import { ReportsPage } from './pages/expenses/ReportsPage'
import { SettingsPage } from './pages/expenses/SettingsPage'
import { TransactionsPage } from './pages/expenses/TransactionsPage'
import { AppLayout } from './layouts/AppLayout'
import { ProtectedRoute } from './layouts/ProtectedRoute'
import './App.css'

function App() {
  // TODO(Milestones 2-5): replace this Vite starter screen with the application
  // route tree for auth, overview, transactions, budgets, and reports.
  return <Routes><Route path="/sign-in" element={<AuthPage mode="login" />} /><Route path="/sign-up" element={<AuthPage mode="register" />} /><Route element={<ProtectedRoute />}><Route element={<AppLayout />}><Route path="/" element={<OverviewPage />} /><Route path="/transactions" element={<TransactionsPage />} /><Route path="/categories" element={<CategoriesPage />} /><Route path="/budgets" element={<BudgetsPage />} /><Route path="/reports" element={<ReportsPage />} /><Route path="/settings" element={<SettingsPage />} /></Route></Route><Route path="*" element={<Navigate to="/" replace />} /></Routes>
}

export default App
