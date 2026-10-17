import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "8"))
CAMPUS_EMERGENCY_NUMBER = os.getenv("CAMPUS_EMERGENCY_NUMBER", "911")
DB_PATH = os.getenv("CAMPUSGUARD_DB", os.path.join(os.path.dirname(os.path.dirname(__file__)), "campusguard.db"))
