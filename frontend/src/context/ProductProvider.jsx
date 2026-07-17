import { useMemo, useState } from 'react'
import { api, setAccessToken } from '../api/client'
import { ProductContext } from './ProductContext'

export const ProductProvider = ({ children }) => {
    // TODO(Milestone 2): define a memoized session context value, fetch the
    // current user, and expose sign-in/sign-out actions to protected routes.
  const [loading, setLoading] = useState(false)
  const [user, setUser] = useState(null)

  async function authenticate(endpoint, values) {
    setLoading(true)
    try {
      // Both register and login return the same session payload.
      const response = await api.post(endpoint, values)
      setAccessToken(response.accessToken)
      setUser(response.user)
      return response.user
    } finally {
      setLoading(false)
    }
  }

  const contextValue = useMemo(() => ({
    user, loading,
    signIn: (values) => authenticate('/auth/login', values),
    signUp: (values) => authenticate('/auth/register', values),
    signOut: () => { setAccessToken(null); setUser(null) },
    updateUser: setUser,
  }), [user, loading])

  return <ProductContext.Provider value={contextValue}>{children}</ProductContext.Provider>
}
