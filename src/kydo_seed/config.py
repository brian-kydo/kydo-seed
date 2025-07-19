from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Defines the application's configuration settings.
    Pydantic automatically reads variables from environment variables
    or a .env file (case-insensitive).
    """
    # Define your settings as class attributes with types.
    # A default value can be provided, e.g., ENVIRONMENT: str = "production"
    GEMINI_API_KEY: str
    GEMINI_MODEL_NAME: str
    GCP_PROJECT: str
    GCP_LOCATION: str
    GCS_LLM_BUCKET_NAME: str

    # This tells Pydantic to load variables from a .env file
    model_config = SettingsConfigDict(env_file=".env")

# Create a single, globally accessible instance of the settings
settings = Settings()
