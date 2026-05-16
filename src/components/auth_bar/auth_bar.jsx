import './auth_bar.css'
import { useState } from 'react'

const AuthBar = ({ user, error, onRegister, onLogin, onLogout }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)

  async function handleLogin(event) {
    event.preventDefault()
    setBusy(true)
    try {
      await onLogin(email, password)
      setPassword('')
    } finally {
      setBusy(false)
    }
  }

  async function handleRegister() {
    setBusy(true)
    try {
      await onRegister(email, password)
      setPassword('')
    } finally {
      setBusy(false)
    }
  }

  async function handleLogout() {
    setBusy(true)
    try {
      await onLogout()
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="auth-bar">
      {user ? (
        <>
          <div className="auth-user">Signed in: <span>{user.email}</span></div>
          <button className="auth-btn" onClick={handleLogout} disabled={busy}>Logout</button>
        </>
      ) : (
        <form className="auth-form" onSubmit={handleLogin}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={busy}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={busy}
          />
          <button type="button" className="auth-btn" onClick={handleRegister} disabled={busy}>Register</button>
          <button type="submit" className="auth-btn" disabled={busy}>Login</button>
        </form>
      )}

      {error && <div className="auth-error">{error}</div>}
    </div>
  )
}

export default AuthBar
