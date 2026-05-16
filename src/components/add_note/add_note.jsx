import "./add_note.css";
import { useState } from "react";
import CreateNote from "../create_note/create_note.jsx";

const AddNote = ({ onSave }) => {
    const [showComponent, setShowComponent] = useState(false);
    return (
        <div className="add-note">
            <button className="add-btn" onClick={() => setShowComponent(true)}>
                <img src="/plus.png" alt="Add Note"/>
            </button>
             {showComponent && <CreateNote onClose={() => setShowComponent(false)} onSave={onSave} />}
        </div>
    )
}

export default AddNote;