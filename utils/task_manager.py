import uuid
from datetime import datetime
import streamlit as st

class TaskManager:
    @staticmethod
    def get_tasks():
        if "tasks" not in st.session_state:
            st.session_state.tasks = []
        return st.session_state.tasks

    @staticmethod
    def add_task(title: str, due_date: str = None):
        tasks = TaskManager.get_tasks()
        new_task = {
            "id": str(uuid.uuid4())[:8],
            "title": title,
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "due_date": due_date
        }
        tasks.append(new_task)
        st.session_state.tasks = tasks
        return new_task

    @staticmethod
    def list_tasks(status_filter: str = "all"):
        tasks = TaskManager.get_tasks()
        if status_filter == "all":
            return tasks
        return [t for t in tasks if t["status"] == status_filter]

    @staticmethod
    def complete_task(identifier: str):
        tasks = TaskManager.get_tasks()
        for task in tasks:
            if task["id"] == identifier or task["title"].lower() == identifier.lower():
                task["status"] = "completed"
                st.session_state.tasks = tasks
                return True
        return False

    @staticmethod
    def delete_task(identifier: str):
        tasks = TaskManager.get_tasks()
        initial_length = len(tasks)
        tasks = [t for t in tasks if t["id"] != identifier and t["title"].lower() != identifier.lower()]
        st.session_state.tasks = tasks
        return len(tasks) < initial_length
