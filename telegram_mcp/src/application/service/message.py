from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from src.application.port.input.message import MessageRetrievalUseCase
from src.application.port.output.message import MessagePort
from src.domain.entities.message import Message


class MessageService(MessageRetrievalUseCase):
    """
    Message 조회를 담당하는 Service
    """

    def __init__(self, message_repository: MessagePort):
        """
        MessageService 초기화
        """
        self.message_repository = message_repository

    async def get_latest_message(self, channel_id: str) -> Message:
        """
        채널의 가장 최근 메시지 1개 조회

        Args:
            channel_id: 채널 username (@python) 또는 ID

        Returns:
            Message: 채널의 가장 최근 메시지

        Raises:
            MessageNotFoundError: 채널의 메시지가 없을 경우
        """
        return await self.message_repository.find_latest_by_channel(channel_id)

    async def get_messages_by_date(self, channel_id: str, date: date) -> list[Message]:
        """
        특정 날짜의 채널 메시지 조회

        Args:
            channel_id: 채널 username (@python) 또는 ID
            date: 일자 (YYYY-MM-DD)

        Returns:
            List[Message]: 해당 날짜의 메시지 목록
        """
        start_ts = datetime.combine(date, datetime.min.time()).replace(tzinfo=ZoneInfo("Asia/Seoul"))
        end_ts = start_ts + timedelta(days=1)
        return await self.message_repository.find_by_channel_and_date_range(channel_id, start_ts, end_ts)

    async def get_yesterday_messages(self, channel_id: str) -> list[Message]:
        """
        어제의 채널 메시지 조회

        Args:
            channel_id: 채널 username (@python) 또는 ID

        Returns:
            List[Message]: 어제의 메시지 목록
        """
        end_ts = datetime.now(ZoneInfo("Asia/Seoul")).replace(hour=0, minute=0, second=0, microsecond=0)
        start_ts = end_ts - timedelta(days=1)
        return await self.message_repository.find_by_channel_and_date_range(channel_id, start_ts, end_ts)
