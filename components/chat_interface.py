import streamlit as st
from utils.ai_handler import get_ai_response, parse_task_intent, get_productivity_tips
from utils.task_manager import TaskManager
from utils.goals_tracker import GoalsTracker

def handle_user_input(prompt: str):
    task_intent = parse_task_intent(prompt)
    
    if task_intent.get("action") == "add":
        title = task_intent.get("title")
        due_date = task_intent.get("due_date")
        if title:
            task = TaskManager.add_task(title, due_date)
            return f"✅ Task ditambahkan: **{title}**" + (f" (Due: {due_date})" if due_date else "")
            
    elif task_intent.get("action") == "list":
        tasks = TaskManager.list_tasks("all")
        if not tasks:
            return "Tidak ada task saat ini."
        resp = "Daftar Task:\n"
        for t in tasks:
            resp += f"- [{t['status']}] {t['title']} {f'(Due: {t['due_date']})' if t.get('due_date') else ''}\n"
        return resp
        
    elif task_intent.get("action") == "complete":
        title = task_intent.get("title")
        if title and TaskManager.complete_task(title):
            return f"✅ Task ditandai selesai: **{title}**"
        return f"❌ Tidak menemukan task dengan nama: **{title}**"
        
    elif task_intent.get("action") == "delete":
        title = task_intent.get("title")
        if title and TaskManager.delete_task(title):
            return f"🗑️ Task dihapus: **{title}**"
        return f"❌ Tidak menemukan task dengan nama: **{title}**"

    lower_prompt = prompt.lower()
    if "tips" in lower_prompt and "produktivitas" in lower_prompt:
        tasks = TaskManager.get_tasks()
        completed = len([t for t in tasks if t["status"] == "completed"])
        achieved, _ = GoalsTracker.get_progress()
        return get_productivity_tips(completed, len(tasks), achieved, "User meminta tips secara manual.", st.session_state.style)
        
    return get_ai_response(
        prompt, 
        "Kamu adalah AI Personal Assistant yang cerdas, suportif, dan selalu siap membantu mengelola produktivitas.", 
        st.session_state.style
    )

def render_chat():
    st.title("🤖 Personal Assistant AI")
    st.caption("Kelola tugas, set goals, dan dapatkan insight produktivitas dari AI!")
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Apa yang ingin kamu kelola hari ini?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Memproses..."):
                response = handle_user_input(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
