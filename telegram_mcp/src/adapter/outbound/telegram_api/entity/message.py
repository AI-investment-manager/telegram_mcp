from dataclasses import dataclass
from datetime import datetime

from telethon.tl.types import Message, PeerChannel, PeerChat, PeerUser, TypePeer


@dataclass
class TelegramMessageEntity:
    """
    Telegram API 응답을 도메인 모델로 변환하는 Entity
    """

    id: int
    message: str
    peer_name: str
    peer_id: int
    _ts: datetime

    @classmethod
    def from_telethon(cls, data: Message) -> "TelegramMessageEntity":
        """
        Telegram API 응답을 도메인 모델로 변환하는 Entity

        Args:
            data: Telegram API 응답

        Returns:
            TelegramMessageEntity: 도메인 모델
        """

        def _get_peer_id(peer: TypePeer) -> int:
            peer_info = peer.to_dict()

            if isinstance(peer, PeerUser):
                return peer_info["user_id"]
            if isinstance(peer, PeerChat):
                return peer_info["chat_id"]
            if isinstance(peer, PeerChannel):
                return peer_info["channel_id"]

        return cls(
            id=data.id,
            message=data.message,
            _ts=data.date,
            peer_name=data.peer_id.to_dict()["_"],
            peer_id=_get_peer_id(data.peer_id),
        )
