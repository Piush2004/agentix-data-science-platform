from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Agentix API"
    API_V1_STR: str = "/api/v1"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
