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
