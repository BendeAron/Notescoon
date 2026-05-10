import './note_section.css'
import Note from '../note/note.jsx'

const NoteSection = () => {
    return (
        <div className="note-section">
            <h2>My Notes</h2>
            <div className="notes-container">
                <Note/> 
                <Note/>
                <Note/>
                <Note/>
                <Note/>
                <Note/>
                <Note/>
                <Note/>
                <Note/>
            </div>
        </div>
    )
}

export default NoteSection;