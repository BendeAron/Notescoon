import './note_section.css'
import Note from '../note/note.jsx'

const NoteSection = ({ user, notes, error }) => {
    return (
        <div className="note-section">
            <h2>My Notes</h2>
            <div className="notes-container">
                {!user && <p>Please log in to see your notes.</p>}
                {error && <p>{error}</p>}
                {user && !error && notes.map((n) => (
                    <Note key={n.id} title={n.title} content={n.content} />
                ))}
            </div>
        </div>
    )
}

export default NoteSection;