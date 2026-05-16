import './create_note.css';
import { useState } from 'react';

const CreateNote = ({ onClose, onSave }) => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);

    async function handleSubmit(event) {
        event.preventDefault();
        setSaving(true);
        setError(null);
        try {
            await onSave({ title, content });
            onClose();
        } catch (err) {
            setError(err.message || 'Failed to save note');
        } finally {
            setSaving(false);
        }
    }

    return (
        <div className="blur-background" onClick={onClose}>
            <div className="create-note" onClick={(event) => event.stopPropagation()}>
                <h2>Create a New Note</h2>
                <button className='close-btn' onClick={onClose}>x</button>
                <form className="note-form" onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Title"
                        className="note-title"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        disabled={saving}
                    />
                    <textarea
                        placeholder="Content"
                        className="note-content"
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        disabled={saving}
                    ></textarea>
                    {error && <p className="note-error">{error}</p>}
                    <button type="submit" className="save-button" disabled={saving}>{saving ? 'Saving…' : 'Save Note'}</button>
                </form>
            </div>
        </div>
    )
}

export default CreateNote;