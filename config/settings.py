import os

class Settings:
    """Configuration settings for the agent."""
    
    @property
    def env_name(self) -> str:
        return os.environ.get("ENV_NAME", "production")

settings = Settings()
