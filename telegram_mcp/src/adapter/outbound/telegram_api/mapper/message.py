from dataclasses import dataclass

from src.adapter.outbound.telegram_api.entity.message import TelegramMessageEntity
from src.domain.entities.message import Message


@dataclass
class TelegramMessageMapper:
    """
    Telegram API 응답을 도메인 모델로 변환하는 Mapper
    """

    @staticmethod
    def to_domain(entity: TelegramMessageEntity) -> Message:
        """
        Telegram API 응답을 도메인 모델로 변환
        """
        return Message(
            id=entity.id,
            message=entity.message,
            peer_name=entity.peer_name,
            peer_id=entity.peer_id,
            _ts=entity._ts,
        )
