import pytest
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """프로젝트 루트 경로 반환"""
    return project_root


@pytest.fixture
def mock_telegram_message():
    """공통 텔레그램 메시지 모킹 fixture"""
    from unittest.mock import MagicMock
    from datetime import datetime
    
    mock_message = MagicMock()
    mock_message.id = 12345
    mock_message.message = "테스트 메시지"
    mock_message.date = datetime(2025, 1, 1, 12, 0, 0)
    
    # Peer 정보 모킹
    mock_peer = MagicMock()
    mock_peer.to_dict.return_value = {"_": "PeerChannel", "channel_id": 67890}
    mock_message.peer_id = mock_peer
    
    return mock_message