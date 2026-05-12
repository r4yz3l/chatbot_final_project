import uuid
from datetime import datetime
import streamlit as st

class GoalsTracker:
    @staticmethod
    def get_today_goals():
        if "goals" not in st.session_state:
            st.session_state.goals = []
            
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Filter goals for today, reset if it's a new day (or just keep historical in state)
        today_goals = [g for g in st.session_state.goals if g.get("date") == today]
        return today_goals

    @staticmethod
    def add_goal(goal_text: str):
        today_goals = GoalsTracker.get_today_goals()
        if len(today_goals) >= 3:
            return False, "Maksimal 3 goals per hari sudah tercapai."
            
        today = datetime.now().strftime("%Y-%m-%d")
        new_goal = {
            "id": str(uuid.uuid4())[:8],
            "goal": goal_text,
            "achieved": False,
            "date": today
        }
        st.session_state.goals.append(new_goal)
        return True, "Goal berhasil ditambahkan."

    @staticmethod
    def toggle_goal(goal_id: str, achieved: bool):
        for goal in st.session_state.goals:
            if goal["id"] == goal_id:
                goal["achieved"] = achieved
                return True
        return False
        
    @staticmethod
    def get_progress():
        today_goals = GoalsTracker.get_today_goals()
        total = len(today_goals)
        if total == 0:
            return 0, 0
        achieved = len([g for g in today_goals if g["achieved"]])
        return achieved, total
