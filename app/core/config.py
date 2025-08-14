from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings loaded from environment variables.
    """
    GOOGLE_API_KEY: str

    # model_config tells Pydantic to load variables from a.env file
    model_config = SettingsConfigDict(env_file=".env")

# Create a single, reusable instance of the settings
settings = Settings()