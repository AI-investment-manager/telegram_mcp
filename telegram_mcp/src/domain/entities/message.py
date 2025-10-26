from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Message:
    """
    텔레그램 메시지 도메인 모델
    """

    id: int
    message: str
    peer_name: str
    peer_id: int
    _ts: datetime

    def to_dict(self) -> dict:
        """
        Message를 딕셔너리로 변환
        """
        return {
            "id": self.id,
            "message": self.message,
            "ts": self.ts,
            "peer_id": self.peer_id,
            "peer_name": self.peer_name,
        }

    @property
    def ts(self) -> datetime:
        """
        Message의 타임스탬프
        """
        return self._ts.astimezone(ZoneInfo("Asia/Seoul"))
