import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# ROOT_DIR_PATH = Path(__file__).parent.parent.parent
# CONFIG_PATH = os.getenv("CONFIG_PATH", ROOT_DIR_PATH / ".env")
load_dotenv()


class Config(BaseSettings):
    """
    Config for the project
    """

    # Telegram 설정
    TELEGRAM_SESSION_NAME: str = "telegram-mcp-session"
    TELEGRAM_API_ID: str = os.getenv("TELEGRAM_API_ID")
    TELEGRAM_API_HASH: str = os.getenv("TELEGRAM_API_HASH")

    def validate(self) -> None:
        """
        Config 유효성 검사
        """
        if not self.TELEGRAM_API_ID:
            raise ValueError("TELEGRAM_API_ID is not set")

        if not self.TELEGRAM_API_HASH:
            raise ValueError("TELEGRAM_API_HASH is not set")
