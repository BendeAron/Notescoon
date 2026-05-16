import "./note.css";

const Note = ({ title, content }) => {
    return (
        <div className="note">
            <h3>{title}</h3>
            <p className="note-content">{content}</p>
        </div>
    )
}

export default Note;