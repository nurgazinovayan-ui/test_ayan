from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_env: str = 'development'
    app_host: str = '0.0.0.0'
    app_port: int = 8000
    database_url: str

    openai_api_key: str = ''
    openai_model: str = 'gpt-4.1-mini'

    telegram_bot_token: str = ''
    telegram_chat_id: str = ''

    instagram_access_token: str = ''
    instagram_business_account_id: str = ''
    instagram_graph_version: str = 'v23.0'

    cloud_storage_provider: str = 'cloudinary'
    cloudinary_cloud_name: str = ''
    cloudinary_api_key: str = ''
    cloudinary_api_secret: str = ''

    s3_bucket_name: str = ''
    s3_region: str = 'us-east-1'
    s3_access_key_id: str = ''
    s3_secret_access_key: str = ''

    hashtags: str = 'aiart,contentcreator'
    competitor_accounts: str = 'examplebrand'
    schedule_cron: str = '0 9 * * *'
    webhook_base_url: str = 'http://localhost:8000'

    @property
    def hashtags_list(self) -> list[str]:
        return [x.strip() for x in self.hashtags.split(',') if x.strip()]

    @property
    def competitor_accounts_list(self) -> list[str]:
        return [x.strip() for x in self.competitor_accounts.split(',') if x.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
