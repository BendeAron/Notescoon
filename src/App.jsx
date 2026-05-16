import './App.css'
import { useEffect, useState } from 'react'
import Navbar from './components/navbar/navbar.jsx'
import AddNote from './components/add_note/add_note.jsx'
import NoteSection from './components/note_section/note_section.jsx'
import AuthBar from './components/auth_bar/auth_bar.jsx'

function App() {
  const [user, setUser] = useState(null)
  const [notes, setNotes] = useState([])
  const [authError, setAuthError] = useState(null)
  const [notesError, setNotesError] = useState(null)

  async function apiRequest(path, options = {}) {
    const res = await fetch(path, {
      credentials: 'include',
      ...options,
      headers: {
        ...(options.headers || {}),
      },
    })

    const text = await res.text()
    let data = null
    if (text) {
      try {
        data = JSON.parse(text)
      } catch {
        data = null
      }
    }

    if (!res.ok) {
      const validationMessage = Array.isArray(data?.detail) && data.detail.length ? data.detail[0]?.msg : null
      const message = data?.error?.message || validationMessage || `Request failed (${res.status})`
      const err = new Error(message)
      err.status = res.status
      err.code = data?.error?.code
      throw err
    }

    return data
  }

  async function loadMe() {
    try {
      const me = await apiRequest('/api/me')
      setUser(me)
      setAuthError(null)
      return me
    } catch (err) {
      if (err.status === 401) {
        setUser(null)
        return null
      }
      setAuthError(err.message)
      return null
    }
  }

  async function loadNotes() {
    try {
      const list = await apiRequest('/api/notes')
      setNotes(list)
      setNotesError(null)
    } catch (err) {
      if (err.status === 401) {
        setNotes([])
        return
      }
      setNotesError(err.message)
    }
  }

  useEffect(() => {
    ;(async () => {
      const me = await loadMe()
      if (me) {
        await loadNotes()
      }
    })()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleRegister(email, password) {
    try {
      const me = await apiRequest('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      setUser(me)
      setAuthError(null)
      await loadNotes()
    } catch (err) {
      setAuthError(err.message)
    }
  }

  async function handleLogin(email, password) {
    try {
      const me = await apiRequest('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })
      setUser(me)
      setAuthError(null)
      await loadNotes()
    } catch (err) {
      setAuthError(err.message)
    }
  }

  async function handleLogout() {
    try {
      await apiRequest('/api/auth/logout', {
        method: 'POST',
      })
      setUser(null)
      setNotes([])
      setAuthError(null)
      setNotesError(null)
    } catch (err) {
      setAuthError(err.message)
    }
  }

  async function handleCreateNote({ title, content }) {
    const note = await apiRequest('/api/notes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    })

    setNotes((prev) => [note, ...prev])
    return note
  }

  return (
    <>
      <Navbar/>
      <AuthBar user={user} error={authError} onRegister={handleRegister} onLogin={handleLogin} onLogout={handleLogout} />
      {user && <AddNote onSave={handleCreateNote} />}
      <NoteSection user={user} notes={notes} error={notesError} />
    </>
  )
}

export default App
