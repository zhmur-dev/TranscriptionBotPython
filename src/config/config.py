from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_API_ID: str = None
    TELEGRAM_API_HASH: str = None
    TELEGRAM_API_URL: str = 'http://telegram_bot_api:8081'
    TG_SERVER_PATH: str = '/var/lib/telegram-bot-api'
    BOT_TOKEN: str = None
    DEEPGRAM_API_KEY: str = None
    TRANSCRIPTION_PATH: str = '/transcriptions/'

    model_config = SettingsConfigDict(
        env_file='creds/.env',
        env_file_encoding='utf-8',
        extra='allow'
    )


settings = Settings()
