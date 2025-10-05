# Telegram Client PRD (Product Requirement Document)

## 📋 개요

**모듈명**: `telegram_client.py`  
**목적**: Telethon 기반 텔레그램 API 클라이언트로 채널 연결, 메시지 수집, 상태 관리 담당  
**위치**: `src/telegram_mcp/telegram_client.py`

---

## 🎯 핵심 요구사항

### 1. 연결 관리
- **연결 설정**: API ID, API Hash, 세션 파일을 통한 인증
- **연결 상태 추적**: 연결/비연결 상태 관리
- **자동 재연결**: 네트워크 장애 시 자동 재연결 로직
- **안전한 종료**: 리소스 정리 및 세션 저장

### 2. 메시지 수집
- **실시간 모니터링**: 새 메시지 실시간 수집
- **배치 수집**: 특정 시간 범위 내 메시지 수집
- **미디어 다운로드**: 이미지, 동영상, 문서 파일 다운로드
- **메타데이터 수집**: 발신자, 채널, 포워딩 정보 등

### 3. 채널 관리
- **채널 정보 조회**: 제목, 참여자 수, 설명 등
- **채널 유효성 검증**: 접근 가능한 채널인지 확인
- **다중 채널 지원**: 여러 채널 동시 모니터링

---

## 🏗️ 클래스 설계

```python
class TelegramClient:
    """Telethon 기반 텔레그램 클라이언트"""
    
    # 초기화
    def __init__(self, api_id: int, api_hash: str, session_name: str)
    
    # 연결 관리
    async def connect(self) -> bool
    async def disconnect(self) -> bool
    def is_connected(self) -> bool
    async def ensure_connected(self) -> bool
    
    # 채널 관리
    async def get_channel_info(self, channel_username: str) -> Dict[str, Any]
    async def validate_channel_access(self, channel_username: str) -> bool
    async def get_channel_entity(self, channel_username: str) -> Channel
    
    # 메시지 수집
    async def collect_messages(
        self, 
        channel: str, 
        start_time: datetime, 
        end_time: datetime, 
        limit: int = 10000
    ) -> List[Dict[str, Any]]
    
    async def get_latest_messages(
        self, 
        channel: str, 
        limit: int = 100
    ) -> List[Dict[str, Any]]
    
    # 실시간 모니터링
    async def start_monitoring(
        self, 
        channels: List[str], 
        callback: Callable
    ) -> None
    
    async def stop_monitoring(self) -> None
    
    # 미디어 처리
    async def download_media(
        self, 
        message: Message, 
        download_path: str
    ) -> Optional[str]
    
    # 유틸리티
    def _format_message(self, message: Message) -> Dict[str, Any]
    def _get_media_info(self, message: Message) -> Dict[str, Any]
    async def _handle_rate_limit(self, func, *args, **kwargs)
```

---

## 📊 데이터 구조

### 메시지 데이터 형식
```python
{
    'message_id': int,
    'channel_username': str,
    'channel_title': str,
    'text': str,
    'timestamp': datetime,
    'sender_user_id': Optional[int],
    'sender_username': Optional[str],
    'sender_first_name': Optional[str],
    'forward_from_channel': Optional[str],
    'forward_original_date': Optional[datetime],
    'reply_to_message_id': Optional[int],
    'media_type': Optional[str],  # 'photo', 'video', 'document', 'audio'
    'media_file_path': Optional[str],
    'collected_at': datetime,
    'collection_batch_id': str
}
```

### 채널 정보 형식
```python
{
    'channel_username': str,
    'channel_title': str,
    'channel_id': int,
    'participants_count': int,
    'description': str,
    'is_verified': bool,
    'last_updated': datetime,
    'access_hash': int
}
```

---

## 🔧 주요 기능 명세

### 1. 연결 관리 (`connect()`)
```python
async def connect(self) -> bool:
    """
    텔레그램에 연결합니다.
    
    Returns:
        bool: 연결 성공 여부
        
    Raises:
        TelegramConnectionError: 연결 실패 시
    """
    # 1. Telethon 클라이언트 초기화
    # 2. 세션 파일 확인 및 로드
    # 3. 전화번호/2FA 인증 처리
    # 4. 연결 상태 업데이트
    # 5. 연결 성공 로깅
```

### 2. 메시지 수집 (`collect_messages()`)
```python
async def collect_messages(
    self, 
    channel: str, 
    start_time: datetime, 
    end_time: datetime, 
    limit: int = 10000
) -> List[Dict[str, Any]]:
    """
    특정 시간 범위의 메시지를 수집합니다.
    
    Args:
        channel: 채널 username (@제외)
        start_time: 수집 시작 시간 (UTC)
        end_time: 수집 종료 시간 (UTC)
        limit: 최대 메시지 수
        
    Returns:
        List[Dict]: 메시지 데이터 리스트
        
    Raises:
        ChannelNotFoundError: 채널이 존재하지 않음
        AccessDeniedError: 채널 접근 권한 없음
        RateLimitError: API 호출 한도 초과
    """
    # 1. 채널 엔티티 조회
    # 2. 시간 범위 검증
    # 3. 배치 단위로 메시지 수집
    # 4. 메시지 포맷팅
    # 5. Rate limit 처리
    # 6. 진행률 로깅
```

### 3. 실시간 모니터링 (`start_monitoring()`)
```python
async def start_monitoring(
    self, 
    channels: List[str], 
    callback: Callable[[Dict[str, Any]], None]
) -> None:
    """
    실시간 메시지 모니터링을 시작합니다.
    
    Args:
        channels: 모니터링할 채널 리스트
        callback: 새 메시지 처리 콜백 함수
        
    Raises:
        MonitoringError: 모니터링 시작 실패
    """
    # 1. 채널 유효성 검증
    # 2. Event handler 등록
    # 3. 백그라운드 태스크 시작
    # 4. 모니터링 상태 업데이트
    # 5. 에러 핸들링 및 재시도
```

---

## 🛡️ 에러 처리

### 커스텀 예외 클래스
```python
class TelegramClientError(Exception):
    """텔레그램 클라이언트 기본 예외"""
    pass

class TelegramConnectionError(TelegramClientError):
    """연결 관련 예외"""
    pass

class ChannelNotFoundError(TelegramClientError):
    """채널을 찾을 수 없음"""
    pass

class AccessDeniedError(TelegramClientError):
    """채널 접근 권한 없음"""
    pass

class RateLimitError(TelegramClientError):
    """API 호출 한도 초과"""
    pass

class MonitoringError(TelegramClientError):
    """모니터링 관련 예외"""
    pass
```

### 에러 핸들링 전략
- **Rate Limit**: 지수 백오프로 재시도
- **Network Error**: 자동 재연결 시도
- **Access Denied**: 명확한 에러 메시지 제공
- **Session Expired**: 재인증 요청

---

## 🔄 상태 관리

### 연결 상태
```python
class ConnectionStatus(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"  
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    ERROR = "error"
```

### 모니터링 상태
```python
class MonitoringStatus(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"
```

---

## 📝 구현 가이드

### 1. 기본 구조 생성
- 클래스 정의 및 초기화
- 필수 import 문 추가
- 로깅 설정

### 2. 연결 관리 구현
- Telethon 클라이언트 초기화
- 인증 처리 (전화번호, 2FA)
- 연결 상태 추적

### 3. 메시지 수집 구현
- 채널 엔티티 조회
- 시간 기반 메시지 필터링
- 배치 처리 로직

### 4. 실시간 모니터링 구현
- 이벤트 핸들러 등록
- 백그라운드 태스크 관리
- 콜백 함수 처리

### 5. 미디어 처리 구현
- 파일 다운로드
- 파일명 생성
- 저장 경로 관리

### 6. 에러 처리 및 재시도 로직
- 커스텀 예외 정의
- Rate limit 핸들링
- 자동 재연결

---

## 🧪 테스트 케이스

### 단위 테스트
- 연결/해제 테스트
- 메시지 포맷팅 테스트
- 채널 유효성 검증 테스트

### 통합 테스트
- 실제 채널 메시지 수집
- 실시간 모니터링 테스트
- 에러 시나리오 테스트

### 성능 테스트
- 대량 메시지 수집
- 메모리 사용량 모니터링
- Rate limit 처리 검증

---

## 🔗 의존성

### 외부 라이브러리
- `telethon`: 텔레그램 API 클라이언트
- `asyncio`: 비동기 처리
- `datetime`: 시간 처리
- `logging`: 로깅
- `pathlib`: 파일 경로 처리

### 내부 모듈
- `utils.py`: 유틸리티 함수
- 환경변수에서 API 키 로드

---

## 📊 성능 최적화

### 메모리 관리
- 대량 메시지 스트리밍 처리
- 불필요한 객체 즉시 해제
- 메모리 사용량 모니터링

### 네트워크 최적화
- 배치 요청으로 API 호출 최소화
- 연결 풀링 활용
- 압축 전송 사용

### 비동기 처리
- 여러 채널 동시 처리
- 메시지 수집과 저장 파이프라이닝
- 백그라운드 작업 분리

---

## 📋 체크리스트

### Phase 1: 기본 구조
- [ ] 클래스 및 초기화 메서드
- [ ] 연결 관리 메서드
- [ ] 기본 에러 처리

### Phase 2: 메시지 수집
- [ ] 배치 메시지 수집
- [ ] 메시지 포맷팅
- [ ] 채널 정보 조회

### Phase 3: 실시간 모니터링  
- [ ] 이벤트 핸들러
- [ ] 백그라운드 태스크
- [ ] 상태 관리

### Phase 4: 고급 기능
- [ ] 미디어 다운로드
- [ ] Rate limit 처리
- [ ] 자동 재연결

### Phase 5: 테스트 및 최적화
- [ ] 단위 테스트
- [ ] 성능 최적화
- [ ] 문서화

---

## 🚀 다음 단계

1. **telegram_client.py 구현** (이 PRD 기반)
2. **parquet_storage.py 구현** (Parquet 저장 로직)
3. **message_collector.py 구현** (수집 스케줄러)
4. **mcp_tools.py 구현** (MCP 도구 인터페이스)

---

*이 PRD를 참고하여 telegram_client.py를 단계적으로 구현하세요. 각 단계마다 테스트를 통해 검증하고 다음 단계로 진행하는 것을 권장합니다.*