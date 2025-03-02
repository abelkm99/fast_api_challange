import os
from enum import Enum
from typing import Any

from pydantic import BaseModel


class EnvironmentOption(Enum):
    DEVELOPMENT = 1
    TESTING = 2
    STAGING = 3
    PRODUCTION = 4

    @classmethod
    def get(cls, env: str):
        for option in cls:
            if option.name.lower() == env.lower():
                return option
        raise ValueError(f"Invalid environment option: {env}")

    def __lt__(self, other: Any):
        if isinstance(other, EnvironmentOption):
            return self.value < other.value
        return False

    def __le__(self, other: Any):
        if isinstance(other, EnvironmentOption):
            return self.value <= other.value
        return False

    def __gt__(self, other: Any):
        if isinstance(other, EnvironmentOption):
            return self.value > other.value
        return False

    def __ge__(self, other: Any):
        if isinstance(other, EnvironmentOption):
            return self.value >= other.value
        return False

    def __eq__(self, other: Any):
        if isinstance(other, EnvironmentOption):
            return self.value == other.value
        return False


class Settings(BaseModel):
    APP_NAME: str = "AI underwritter"
    APP_VERSION: str = "0.1.0"


class CryptSettings(BaseModel):
    JWT_SECRET: str = os.environ.get("JWT_SECRET", default="jwt_secret")
    SECRET_KEY: str = os.environ.get("SECRET_KEY", default="secret")
    ALGORITHM: str = os.environ.get("ALGORITHM", default="HS256")


class EnvironmentSettings(BaseModel):
    # change the development mood from here
    ENVIRONMENT: EnvironmentOption = EnvironmentOption.get(os.environ.get("ENVIRONMENT", "development"))


class CorsSettings(BaseModel):
    CORS_ORIGINS: list[str] = ["*"]


class OAuthSettings(BaseModel):
    """OAuth settings"""

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.environ.get(
            "ACCESS_TOKEN_EXPIRE_MINUTES",
            default=str(100000),
        )
    )
    OTP_EXPIRE_MINUTES: int = int(
        os.environ.get(
            "OTP_EXPIRE_MINUTES",
            default=str(30),
        )
    )

    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS ", 30))


class DatabaseSettings(BaseModel):
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
    DATABASE_POOL_RECYCLE: int = int(os.environ.get("DATABASE_POOL_RECYCLE", 900))
    DATABASE_POOL_SIZE: int = int(os.environ.get("DATABASE_POOL_SIZE", 20))
    DATABASE_POOL_OVERFLOW: int = int(os.environ.get("DATABASE_POOL_OVERFLOW", 20))


class LoggerLevel(BaseModel):
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")


class OtelConfig(BaseModel):
    OTEL_EXPORTER_ENDPOINT: str = os.environ.get("OTEL_EXPORTER_ENDPOINT", "http://localhost:4317")
    ENABLE_CONSOLE_LOG: bool = bool(os.environ.get("SHOW_OTEL_LOG", False))


class LogFireConfig(BaseModel):
    LOG_FIRE_API_KEY: str = os.environ.get("LOG_FIRE_API_KEY", "")


class BaseConfig(
    EnvironmentSettings,
    LoggerLevel,
    Settings,
    CryptSettings,
    CorsSettings,
    OAuthSettings,
    DatabaseSettings,
    OtelConfig,
    LogFireConfig,
):
    SFRANALYTICS_API_KEY: str = os.environ.get("SFRANALYTICS_API_KEY", "")

    def get_env(self, environment_option: EnvironmentOption | None = None):
        if environment_option:
            self.ENVIRONMENT = environment_option
        if self.ENVIRONMENT == EnvironmentOption.PRODUCTION:
            return ProdConfig()
        if self.ENVIRONMENT == EnvironmentOption.TESTING:
            return TestConfig()
        if self.ENVIRONMENT == EnvironmentOption.STAGING:
            return StagingConfig()
        return DevConfig()


class ProdConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get(
        "PRODUCTION_DATABASE_URL",
        default="",
    )

    def __call__(self) -> Any:
        os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment.name=prod"


class DevConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get(
        "DEVELOPMENT_DATABASE_URL",
        default="",
    )
    LOGFIRE_SEND_TO_LOGFIRE: bool = False

    def __call__(self) -> Any:
        os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment.name=dev"


class TestConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get(
        "TEST_DATABASE_URL",
        default="",
    )

    def __call__(self) -> Any:
        os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment.name=testing"


class StagingConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get(
        "STAGING_DATABASE_URL",
        default="",
    )

    def __call__(self) -> Any:
        os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment.name=staging"


MySettings = BaseConfig().get_env()
MySettings()
