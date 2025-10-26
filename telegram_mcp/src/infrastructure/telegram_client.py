from typing import Optional

from telethon import TelegramClient as TelethonClient


class TelegramClient:
    """
    텔레그램 클라이언트 세션 관리
    """

    def __init__(self, session_name: str, api_id: str, api_hash: str):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self._client: Optional[TelethonClient] = None

    async def connect(self) -> None:
        """
        텔레그램 클라이언트 연결
        """
        if self._client is None:
            self._client = TelethonClient(
                session=self.session_name,
                api_id=self.api_id,
                api_hash=self.api_hash,
            )

        if not self._client.is_connected():
            await self._client.start()
            print("텔레그램 클라이언트 연결 완료")

    async def disconnect(self) -> None:
        """
        텔레그램 클라이언트 연결 해제
        """
        if self._client and self._client.is_connected():
            print("disconnect")
            await self._client.disconnect()
            print("텔레그램 클라이언트 연결 해제 완료")

    def is_connected(self) -> bool:
        """
        연결 상태 확인
        """
        return self._client is not None and self._client.is_connected()

    @property
    def client(self) -> TelethonClient:
        """
        내부 텔레그램 클라이언트 반환
        """
        if self._client is None:
            raise RuntimeError("클라이언트가 초기화되지 않았습니다. connect()를 먼저 호출하세요.")
        return self._client

    async def __aenter__(self):
        """
        비동기 컨텍스트 매니저 진입
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        비동기 컨텍스트 매니저 종료
        """
        print("__aexit__")
        await self.disconnect()
