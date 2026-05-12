import streamlit as st
from utils.ai_handler import get_ai_response
from utils.task_manager import TaskManager
import pandas as pd
from datetime import datetime, timedelta

def generate_weekly_review(style: str) -> str:
    # 1. Gather Tasks Data (for the past 7 days)
    tasks = TaskManager.get_tasks()
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    recent_tasks = [t for t in tasks if t["created_at"] >= seven_days_ago]
    completed_tasks = len([t for t in recent_tasks if t["status"] == "completed"])
    total_tasks = len(recent_tasks)
    
    task_summary = f"Total tasks minggu ini: {total_tasks}. Selesai: {completed_tasks}."
    for t in recent_tasks:
        task_summary += f"\n- {t['title']} ({t['status']})"
        
    # 2. Gather Goals Data
    goals = st.session_state.get("goals", [])
    recent_goals = [g for g in goals if g.get("date", "") >= seven_days_ago]
    achieved_goals = len([g for g in recent_goals if g["achieved"]])
    total_goals = len(recent_goals)
    
    goals_summary = f"Total goals minggu ini: {total_goals}. Tercapai: {achieved_goals}."
    for g in recent_goals:
        status_text = "Tercapai" if g["achieved"] else "Belum"
        goals_summary += f"\n- [{g['date']}] {g['goal']} ({status_text})"

    # 3. Gather Notes Data
    notes = st.session_state.get("notes", [])
    recent_notes = [n for n in notes if n["timestamp"].split()[0] >= seven_days_ago]
    
    notes_summary = f"Total notes minggu ini: {len(recent_notes)}."
    for n in recent_notes:
        notes_summary += f"\n- {n['content']}"
        
    prompt = f"""
    Kamu adalah productivity coach. Berdasarkan data berikut dari minggu ini:

    TASKS:
    {task_summary}

    DAILY GOALS:
    {goals_summary}

    NOTES:
    {notes_summary}

    Buatkan weekly review yang mencakup:
    1. Ringkasan pencapaian minggu ini
    2. Persentase completion rate
    3. Insight atau pola yang kamu temukan
    4. Rekomendasi konkret untuk minggu depan
    """
    
    return get_ai_response(prompt, "You are a professional productivity coach.", style, temperature=0.8)
