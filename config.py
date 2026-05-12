import os
from dotenv import load_dotenv

load_dotenv()

# Load from environment or Streamlit secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Will use gemini-2.5-flash as the fast/lite model for genai sdk
MODEL_NAME = "gemini-2.5-flash"

GENERATION_CONFIG = {
    "temperature": 0.7,        # Balanced creativity
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 1024,
}
