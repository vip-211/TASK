
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"
    log_dir: str = "logs"
    
    class Config:
        env_file = ".env"


settings = Settings()
