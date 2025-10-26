from dependency_injector import containers, providers
from src.adapter.outbound.telegram_api.repository.message import TelegramMessageRepository
from src.application.service.message import MessageService
from src.infrastructure.config import Config
from src.infrastructure.telegram_client import TelegramClient


class Container(containers.DeclarativeContainer):
    """
    애플리케이션의 의존성 주입 컨테이너
    """

    wiring_config = containers.WiringConfiguration(modules=["src.adapter.inbound.web.routes.message"])

    config = providers.Singleton(Config)

    telegram_client = providers.Singleton(
        TelegramClient,
        session_name=config.provided.TELEGRAM_SESSION_NAME,
        api_id=config.provided.TELEGRAM_API_ID,
        api_hash=config.provided.TELEGRAM_API_HASH,
    )

    message_repository = providers.Singleton(
        TelegramMessageRepository,
        telegram_client=telegram_client,
    )

    message_service = providers.Factory(
        MessageService,
        message_repository=message_repository,
    )
