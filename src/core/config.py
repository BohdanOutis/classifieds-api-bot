import tomllib
from enum import StrEnum
from pathlib import Path
from typing import Any, Tuple, Type

from pydantic import BaseModel, SecretStr
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class LogRenderer(StrEnum):
    JSON = "json"
    CONSOLE = "console"


class BotConfig(BaseModel):
    token: SecretStr


class DbConfig(BaseModel):
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: SecretStr
    name: str = "classifieds_db"

    @property
    def build_url(self) -> str:
        pwd = self.password.get_secret_value()
        return f"postgresql+asyncpg://{self.user}:{pwd}@{self.host}:{self.port}/{self.name}"


class WpConfig(BaseModel):
    url: str
    user: str
    application_password: SecretStr


class PortmoneConfig(BaseModel):
    payee_id: int
    gateway_url: str
    secret_key: SecretStr


class ApiConfig(BaseModel):
    base_url: str = "http://api:8000/api/v1"


class LogConfig(BaseModel):
    project_name: str = "Epstein"
    show_datetime: bool = True
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
    show_debug_logs: bool = True
    time_in_utc: bool = False
    use_colors_in_console: bool = True
    renderer: LogRenderer = LogRenderer.CONSOLE
    allow_third_party_logs: bool = False


class TomlConfigSettingsSource(PydanticBaseSettingsSource):
    def get_field_value(
        self, field: Any, field_name: str
    ) -> Tuple[Any, str, bool]:
        return None, field_name, False

    def __call__(self) -> dict[str, Any]:
        file_path = Path.cwd() / "settings.toml"
        if not file_path.exists():
            file_path = Path(__file__).resolve().parent.parent.parent / "settings.toml"
            if not file_path.exists():
                return {}

        with file_path.open("rb") as f:
            return tomllib.load(f)


class Settings(BaseSettings):
    bot: BotConfig
    db: DbConfig
    wp: WpConfig
    api: ApiConfig
    logs: LogConfig
    portmone: PortmoneConfig

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls),
        )


config = Settings()