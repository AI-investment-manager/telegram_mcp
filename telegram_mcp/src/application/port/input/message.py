from abc import ABC, abstractmethod
from datetime import date

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

    @abstractmethod
    async def get_messages_by_date(self, channel_id: str, date: date) -> list[Message]:
        """
        특정 날짜의 채널 메시지 조회

        Args:
            channel_id: 채널 username (@python) 또는 ID
            date: 일자 (YYYY-MM-DD)

        Returns:
            List[Message]: 해당 날짜의 메시지 목록
        """

    @abstractmethod
    async def get_yesterday_messages(self, channel_id: str) -> list[Message]:
        """
        어제의 채널 메시지 조회

        Args:
            channel_id: 채널 username (@python) 또는 ID

        Returns:
            List[Message]: 어제의 메시지 목록
        """
