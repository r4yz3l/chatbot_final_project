import json
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, MODEL_NAME, GENERATION_CONFIG

client = genai.Client(api_key=GEMINI_API_KEY)

def get_ai_response(prompt: str, system_instruction: str, style: str, temperature: float = None) -> str:
    """
    Send a prompt to Gemini and return the text response.
    """
    temp = temperature if temperature is not None else GENERATION_CONFIG["temperature"]
    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=f"{system_instruction}\n\nGaya bahasa: {style}",
                temperature=temp,
                top_p=GENERATION_CONFIG["top_p"],
                top_k=GENERATION_CONFIG["top_k"],
                max_output_tokens=GENERATION_CONFIG["max_output_tokens"],
            ),
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"⚠️ **Server AI sedang sibuk/penuh (Error 503)**.\n\nSistem Google Gemini saat ini sedang melayani terlalu banyak permintaan. Silakan tunggu beberapa detik dan coba lagi, atau Anda bisa mengubah `MODEL_NAME` di file `config.py` kembali ke `gemini-2.5-flash`."

def parse_task_intent(user_input: str) -> dict:
    """
    Use Gemini to parse free-text input into structured task action.
    Returns dict with keys: action, title, due_date
    """
    prompt = f"""
    Parse input berikut menjadi JSON aksi task management.
    Input: "{user_input}"
    
    PENTING: Jika input BUKAN perintah untuk mengelola task (misalnya pengguna hanya bertanya, minta tips, atau ngobrol biasa), kembalikan action "chat".
    
    Return JSON dengan format:
    {{"action": "add|list|complete|delete|chat", "title": "...", "due_date": "YYYY-MM-DD or null"}}
    
    Hanya return JSON, tanpa penjelasan tambahan.
    """
    # Use low temperature for deterministic JSON parsing
    response = get_ai_response(prompt, "You are a JSON parser.", "Formal", temperature=0.1)
    
    # Parse JSON from response
    try:
        # Clean up potential markdown formatting around the JSON
        clean_response = response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]
        elif clean_response.startswith("```"):
            clean_response = clean_response[3:]
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]
            
        parsed = json.loads(clean_response.strip())
        
        # If AI returned a list instead of dict, extract the first element
        if isinstance(parsed, list) and len(parsed) > 0:
            return parsed[0]
        elif isinstance(parsed, dict):
            return parsed
        else:
            return {"action": "error", "message": "Gagal memahami maksud task (format salah)."}
    except Exception as e:
        print(f"Failed to parse task intent: {e}, Response: {response}")
        return {"action": "error", "message": "Gagal memahami maksud task."}

def get_productivity_tips(completed_today: int, total_today: int, goals_achieved: int, user_context: str, style: str) -> str:
    """
    Get productivity tips from Gemini based on user's current context.
    """
    prompt = f"""
    Kamu adalah productivity coach yang supportif.

    Konteks pengguna saat ini:
    - Tasks selesai hari ini: {completed_today}/{total_today}
    - Goals tercapai: {goals_achieved}/3
    - Mood/konteks tambahan: {user_context}

    Berikan:
    1. Satu motivasi singkat yang relevan dengan kondisi ini
    2. 2-3 tips produktivitas spesifik dan actionable
    3. Teknik fokus yang bisa langsung dicoba (misal: Pomodoro, time-blocking)

    Respons maksimal 200 kata.
    """
    return get_ai_response(prompt, "You are a helpful productivity coach.", style, temperature=0.8)
