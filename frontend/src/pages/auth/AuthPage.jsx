import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Status } from '../../components/shared/Status'
import { useProductContext } from '../../context/UseProductContext'

export function AuthPage({ mode }) {
  const registering = mode === 'register'
  const [values, setValues] = useState({ displayName: '', email: '', password: '' })
  const [message, setMessage] = useState('')
  const navigate = useNavigate()
  const { signIn, signUp, loading } = useProductContext()
  async function submit(event) {
    event.preventDefault(); setMessage('')
    try { await (registering ? signUp(values) : signIn(values)); navigate('/') }
    catch (problem) { setMessage(problem.error || 'Could not sign you in.') }
  }
  return <main className="auth"><form onSubmit={submit}><h1>{registering ? 'Create your account' : 'Welcome back'}</h1>{message && <Status type="error">{message}</Status>}{registering && <label>Name<input required value={values.displayName} onChange={(e) => setValues({ ...values, displayName: e.target.value })} /></label>}<label>Email<input type="email" required value={values.email} onChange={(e) => setValues({ ...values, email: e.target.value })} /></label><label>Password<input type="password" minLength="8" required value={values.password} onChange={(e) => setValues({ ...values, password: e.target.value })} /></label><button disabled={loading}>{loading ? 'Please wait…' : registering ? 'Create account' : 'Sign in'}</button><p>{registering ? 'Already registered?' : 'Need an account?'} <Link to={registering ? '/sign-in' : '/sign-up'}>{registering ? 'Sign in' : 'Sign up'}</Link></p></form></main>
}
