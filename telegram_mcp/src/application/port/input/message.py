from abc import ABC, abstractmethod

from src.domain.entities.message import Message


class MessageRetrievalUseCase(ABC):
    """
    Message 조회를 담당하는 Use Case
    """

    @abstractmethod
    async def get_latest_message(self, channel_id: str) -> Message:
        """
        Message 조회

        Args:
            channel_id: 채널 username (@python) 또는 ID

        Returns:
            Message: 채널의 가장 최근 메시지

        Raises:
            MessageNotFoundError: 채널의 메시지가 없을 경우
        """
