import './App.css'
import Navbar from './components/navbar/navbar.jsx'
import AddNote from './components/add_note/add_note.jsx'
import NoteSection from './components/note_section/note_section.jsx'

function App() {

  return (
    <>
      <Navbar/>
      <AddNote/>
      <NoteSection/>
    </>
  )
}

export default App
