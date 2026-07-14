# Refactored wrapper reusing original ai_service.py logic
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from ai_service import OllamaService

# Central singleton instance
ollama_service = OllamaService()
