import { Navigate, Outlet } from 'react-router-dom'
import { useProductContext } from '../context/UseProductContext'

export function ProtectedRoute() {
  const { user } = useProductContext()
  // Redirecting at the route boundary prevents private screens from rendering first.
  return user ? <Outlet /> : <Navigate to="/sign-in" replace />
}
