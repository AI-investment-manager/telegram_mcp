from abc import ABC, abstractmethod

from src.domain.entities.message import Message


class MessagePort(ABC):
    """
    메시지 조회를 담당하는 Output Port

    Application이 외부(Telegram API)에 요구하는 인터페이스
    """

    @abstractmethod
    async def find_latest_by_channel(self, channel_id: str) -> Message:
        """
        채널의 가장 최근 메시지 1개 조회

        Args:
            channel_id: 채널 username (@python) 또는 ID

        Returns:
            Message: 채널의 가장 최근 메시지

        Raises:
            MessageNotFoundError: 채널의 메시지가 없을 경우
        """
