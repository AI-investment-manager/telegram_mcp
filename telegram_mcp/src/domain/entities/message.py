from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Message:
    """
    텔레그램 메시지 도메인 모델
    """

    id: int
    message: str
    date: datetime
    peer_name: str
    peer_id: int

    def to_dict(self) -> dict:
        """
        Message를 딕셔너리로 변환
        """
        return {
            "id": self.id,
            "message": self.message,
            "date": self.date,
            "peer_id": self.peer_id,
        }
