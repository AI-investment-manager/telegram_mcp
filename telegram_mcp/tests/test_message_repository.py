import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.adapter.outbound.telegram_api.repository.message import TelegramMessageRepository
from src.domain.entities.message import Message
from src.infrastructure.exception import MessageNotFoundError


class TestTelegramMessageRepository:
    """TelegramMessageRepository 단위 테스트"""

    @pytest.fixture
    def mock_telegram_client(self):
        """텔레그램 클라이언트 모킹"""
        mock_client = AsyncMock()
        # Context manager 지원을 위한 설정
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        return mock_client

    @pytest.fixture
    def repository(self, mock_telegram_client):
        """테스트용 리포지토리 인스턴스"""
        return TelegramMessageRepository(mock_telegram_client)

    @pytest.fixture
    def sample_message_data(self):
        """테스트용 메시지 데이터"""
        from telethon.tl.types import PeerChannel
        
        mock_message = MagicMock()
        mock_message.id = 12345
        mock_message.message = "테스트 메시지 내용"
        mock_message.date = datetime(2025, 1, 1, 12, 0, 0)
        
        # Peer 정보 모킹 - 실제 PeerChannel 타입으로 설정
        mock_peer = MagicMock(spec=PeerChannel)
        mock_peer.to_dict.return_value = {"_": "PeerChannel", "channel_id": 67890}
        mock_message.peer_id = mock_peer
        
        return mock_message

    @pytest.mark.asyncio
    async def test_find_latest_by_channel_success(self, repository, mock_telegram_client, sample_message_data):
        """채널에서 최신 메시지 조회 성공 테스트"""
        # Given
        channel_id = "@test_channel"
        mock_telegram_client.get_messages.return_value = [sample_message_data]
        
        # When
        result = await repository.find_latest_by_channel(channel_id)
        
        # Then
        assert isinstance(result, Message)
        assert result.id == 12345
        assert result.message == "테스트 메시지 내용"
        assert result.date == datetime(2025, 1, 1, 12, 0, 0)
        assert result.peer_name == "PeerChannel"
        assert result.peer_id == 67890
        
        # 텔레그램 클라이언트가 올바른 파라미터로 호출되었는지 확인
        mock_telegram_client.get_messages.assert_called_once_with(channel_id, limit=1)

    @pytest.mark.asyncio
    async def test_find_latest_by_channel_no_messages(self, repository, mock_telegram_client):
        """채널에 메시지가 없을 때 예외 발생 테스트"""
        # Given
        channel_id = "@empty_channel"
        mock_telegram_client.get_messages.return_value = []
        
        # When & Then
        with pytest.raises(MessageNotFoundError) as exc_info:
            await repository.find_latest_by_channel(channel_id)
        
        assert f"채널 {channel_id}의 메시지가 없습니다." in str(exc_info.value)
        mock_telegram_client.get_messages.assert_called_once_with(channel_id, limit=1)

    @pytest.mark.asyncio
    async def test_find_latest_by_channel_none_result(self, repository, mock_telegram_client):
        """메시지 조회 결과가 None일 때 예외 발생 테스트"""
        # Given
        channel_id = "@test_channel"
        mock_telegram_client.get_messages.return_value = None
        
        # When & Then
        with pytest.raises(MessageNotFoundError) as exc_info:
            await repository.find_latest_by_channel(channel_id)
        
        assert f"채널 {channel_id}의 메시지가 없습니다." in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_find_latest_by_channel_with_different_peer_types(self, repository, mock_telegram_client):
        """다양한 피어 타입 처리 테스트"""
        from telethon.tl.types import PeerUser
        
        # Given - PeerUser 타입
        channel_id = "@user_channel"
        mock_message = MagicMock()
        mock_message.id = 111
        mock_message.message = "사용자 메시지"
        mock_message.date = datetime(2025, 1, 2, 10, 0, 0)
        
        mock_peer = MagicMock(spec=PeerUser)
        mock_peer.to_dict.return_value = {"_": "PeerUser", "user_id": 123}
        mock_message.peer_id = mock_peer
        
        mock_telegram_client.get_messages.return_value = [mock_message]
        
        # When
        result = await repository.find_latest_by_channel(channel_id)
        
        # Then
        assert result.peer_name == "PeerUser"
        assert result.peer_id == 123

    @pytest.mark.asyncio
    async def test_repository_initialization(self, mock_telegram_client):
        """리포지토리 초기화 테스트"""
        # When
        repository = TelegramMessageRepository(mock_telegram_client)
        
        # Then
        assert repository.telegram_client == mock_telegram_client

    @pytest.mark.asyncio
    async def test_find_latest_by_channel_with_numeric_channel_id(self, repository, mock_telegram_client, sample_message_data):
        """숫자 형태의 채널 ID로 조회 테스트"""
        # Given
        channel_id = "123456789"
        mock_telegram_client.get_messages.return_value = [sample_message_data]
        
        # When
        result = await repository.find_latest_by_channel(channel_id)
        
        # Then
        assert isinstance(result, Message)
        mock_telegram_client.get_messages.assert_called_once_with(channel_id, limit=1)

    @pytest.mark.asyncio
    async def test_find_latest_by_channel_telegram_api_exception(self, repository, mock_telegram_client):
        """텔레그램 API 호출 시 예외 발생 테스트"""
        # Given
        channel_id = "@error_channel"
        mock_telegram_client.get_messages.side_effect = Exception("API 호출 실패")
        
        # When & Then
        with pytest.raises(Exception) as exc_info:
            await repository.find_latest_by_channel(channel_id)
        
        assert "API 호출 실패" in str(exc_info.value)
