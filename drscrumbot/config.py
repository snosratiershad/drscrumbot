# Copyright (C) 2025  Salar Nosrati-Ershad salar@roverc.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    provides a global config instance
"""
from pydantic import SecretStr, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
        main application configuration using pydantic-settings

        based on 12factor, the production config shall be sotored in env.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    debug: bool = Field(False, description="Debug mode")

    bot_token: SecretStr = Field(..., description="Telegram Bot API token")

    openai_api_key: SecretStr = Field(
        ...,
        description="API Key of OpenAI used in Pydantic AI agents"
    )

    @field_validator("bot_token")
    @classmethod
    def validate_bot_token(cls, v: SecretStr) -> SecretStr:
        """
            validator for bot token

            removes leading and tailing whitespaces and insures that value
            is not empty.
        """
        v: SecretStr = SecretStr(v.get_secret_value().strip())
        if len(v):
            return v
        raise ValueError("BOT_TOKEN cannot be empty")

    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_api_key(cls, v: SecretStr) -> SecretStr:
        """
            validator for OpenAI API key

            removes leading and tailing whitespaces and insures that value
            is not empty.
        """
        v: SecretStr = SecretStr(v.get_secret_value().strip())
        if len(v):
            return v
        raise ValueError("OPENAI_API_KEY cannot be empty")


config: Config = Config()  # it's a global instance
