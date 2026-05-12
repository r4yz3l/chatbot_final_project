import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(env_path, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3-flash-preview"

GENERATION_CONFIG = {
    "temperature": 0.7,        
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1024,
}
