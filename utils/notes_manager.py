import uuid
from datetime import datetime
import streamlit as st
from utils.ai_handler import get_ai_response

class NotesManager:
    @staticmethod
    def get_notes():
        if "notes" not in st.session_state:
            st.session_state.notes = []
        return st.session_state.notes

    @staticmethod
    def add_note(content: str):
        notes = NotesManager.get_notes()
        new_note = {
            "id": str(uuid.uuid4())[:8],
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": None
        }
        notes.append(new_note)
        st.session_state.notes = notes
        return new_note

    @staticmethod
    def delete_note(note_id: str):
        notes = NotesManager.get_notes()
        initial_length = len(notes)
        notes = [n for n in notes if n["id"] != note_id]
        st.session_state.notes = notes
        return len(notes) < initial_length

    @staticmethod
    def organize_notes(style: str):
        notes = NotesManager.get_notes()
        if not notes:
            return "Tidak ada catatan untuk diorganisir."
            
        notes_text = "\n".join([f"- [{n['timestamp']}] {n['content']}" for n in notes])
        
        prompt = f"""
        Berikut adalah daftar catatan cepat pengguna:
        {notes_text}
        
        Tolong:
        1. Kelompokkan notes ke dalam kategori yang relevan (misal: Ide, To-Do, Referensi, Insight)
        2. Buat ringkasan singkat per kategori
        3. Tandai notes mana yang butuh tindak lanjut segera
        """
        
        return get_ai_response(prompt, "You are an intelligent notes organizer.", style, temperature=0.7)
