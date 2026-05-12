import streamlit as st
from utils.goals_tracker import GoalsTracker
from utils.weekly_review import generate_weekly_review
from utils.notes_manager import NotesManager
from utils.task_manager import TaskManager
from utils.ai_handler import get_productivity_tips

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Pengaturan")
        
        # 1. Gaya Bahasa Selector
        st.subheader("Gaya Bahasa AI")
        st.session_state.style = st.selectbox(
            "Pilih gaya respons:",
            ["Formal", "Santai", "Profesional"],
            index=1 # Default Santai
        )
        
        st.divider()
        
        # 2. Daily Goals Tracker
        st.subheader("🎯 Daily Goals")
        today_goals = GoalsTracker.get_today_goals()
        
        # Add new goal form
        if len(today_goals) < 3:
            with st.form("add_goal_form", clear_on_submit=True):
                new_goal = st.text_input("Tambah goal hari ini...")
                submit_goal = st.form_submit_button("Tambah")
                if submit_goal and new_goal:
                    success, msg = GoalsTracker.add_goal(new_goal)
                    if success:
                        st.rerun()
                    else:
                        st.error(msg)
        
        # Progress Bar
        achieved, total = GoalsTracker.get_progress()
        if total > 0:
            st.progress(achieved / total, text=f"{achieved}/{total} Goals Tercapai")
            
        # List goals
        for goal in today_goals:
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                is_checked = st.checkbox("", value=goal["achieved"], key=f"goal_{goal['id']}")
                if is_checked != goal["achieved"]:
                    GoalsTracker.toggle_goal(goal["id"], is_checked)
                    st.rerun()
            with col2:
                if goal["achieved"]:
                    st.markdown(f"~~{goal['goal']}~~")
                else:
                    st.write(goal["goal"])

        st.divider()
        
        # 3. Task Management (Quick View)
        st.subheader("📋 Tasks")
        tasks = TaskManager.list_tasks("pending")
        st.caption(f"{len(tasks)} tasks pending")
        
        st.divider()
        
        # 4. Quick Notes
        st.subheader("📝 Quick Notes")
        with st.form("add_note_form", clear_on_submit=True):
            new_note = st.text_input("Catat sesuatu...")
            submit_note = st.form_submit_button("Simpan")
            if submit_note and new_note:
                NotesManager.add_note(new_note)
                st.rerun()
                
        if st.button("Organize Notes (AI)", use_container_width=True):
            with st.spinner("AI sedang menyusun catatan..."):
                organized = NotesManager.organize_notes(st.session_state.style)
                st.session_state.messages.append({"role": "assistant", "content": organized})
                st.rerun()

        st.divider()
        
        # 5. Productivity Features
        st.subheader("🚀 Productivity")
        
        if st.button("Generate Weekly Review", use_container_width=True):
            with st.spinner("Menganalisis performa mingguan..."):
                review = generate_weekly_review(st.session_state.style)
                st.session_state.messages.append({"role": "assistant", "content": review})
                st.rerun()
                
        if st.button("Minta Tips AI", use_container_width=True):
            with st.spinner("Memikirkan tips..."):
                # Get metrics
                tasks_today = TaskManager.get_tasks()
                completed = len([t for t in tasks_today if t["status"] == "completed"])
                achieved, _ = GoalsTracker.get_progress()
                tips = get_productivity_tips(completed, len(tasks_today), achieved, "Meminta tips via tombol.", st.session_state.style)
                st.session_state.messages.append({"role": "assistant", "content": tips})
                st.rerun()
