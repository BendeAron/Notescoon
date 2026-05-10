import './create_note.css';

const CreateNote = ({ onClose }) => {
    return (
        <div className="blur-background" onClick={onClose}>
            <div className="create-note" onClick={(event) => event.stopPropagation()}>
                <h2>Create a New Note</h2>
                <button className='close-btn' onClick={onClose}>x</button>
                <form className="note-form" onSubmit={(event) => event.preventDefault()}>
                    <input type="text" placeholder="Title" className="note-title"/>
                    <textarea placeholder="Content" className="note-content"></textarea>
                    <button type="submit" className="save-button">Save Note</button>
                </form>
            </div>
        </div>
    )
}

export default CreateNote;