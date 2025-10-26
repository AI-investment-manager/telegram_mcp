from datetime import datetime

from src.adapter.outbound.telegram_api.entity.message import TelegramMessageEntity
from src.adapter.outbound.telegram_api.mapper.message import TelegramMessageMapper
from src.application.port.output.message import MessagePort
from src.domain.entities.message import Message
from src.infrastructure.exception import MessageNotFoundError
from src.infrastructure.telegram_client import TelegramClient


class TelegramMessageRepository(MessagePort):
    """
    Telegram API를 통해 메시지를 조회하는 Repository
    """

    def __init__(self, telegram_client: TelegramClient):
        """
        TelegramMessageRepository 초기화
        """
        self.telegram_client = telegram_client

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
        async with self.telegram_client:
            message = await self.telegram_client.client.get_messages(channel_id, limit=1)

            if not message:
                raise MessageNotFoundError(f"채널 {channel_id}의 메시지가 없습니다.")

            return TelegramMessageMapper.to_domain(TelegramMessageEntity.from_telethon(message[0]))

    async def find_by_channel_and_date_range(
        self, channel_id: str, start_ts: datetime, end_ts: datetime
    ) -> list[Message]:
        """

        Args:
            channel_id (str): _description_
            start_ts (datetime): 시작 타임스탬프
            end_ts (datetime): 종료 타임스탬프

        Returns:
            list[Message]: _description_
        """
        messages = []

        async with self.telegram_client as c:
            async for message in c.client.iter_messages(channel_id, offset_date=end_ts):
                if message.date < start_ts:
                    break
                messages.append(TelegramMessageMapper.to_domain(TelegramMessageEntity.from_telethon(message)))
        return messages
