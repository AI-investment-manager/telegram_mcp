# 📱 Telegram MCP Server

## 📋 프로젝트 개요

텔레그램 채널에서 메시지를 수집하고 Parquet 형태로 저장하는 전용 MCP(Model Context Protocol) 서버입니다.

**핵심 책임 (단일책임원칙):**
- 🔄 텔레그램 채널 연결 및 모니터링
- 📥 메시지 수집 및 Parquet 저장
- 📊 실시간 배치 처리
- 🌐 MCP over SSE 제공

**명확히 하지 않는 것:**
- ❌ 메시지 검색 및 분석 (별도 Analysis MCP 담당)
- ❌ 감정 분석 (별도 Analysis MCP 담당)
- ❌ 티커 추출 (별도 Analysis MCP 담당)  
- ❌ 투자 분석 (별도 Analysis MCP 담당)
- ❌ 복합 데이터베이스 저장 (별도 DB MCP 담당)

**기술 스택:**
- **언어**: Python 3.12+
- **웹 프레임워크**: FastAPI (SSE 엔드포인트)
- **패키지 관리**: uv
- **컨테이너**: Docker
- **프로토콜**: MCP over SSE
- **텔레그램 API**: Telethon
- **데이터 형식**: Parquet (분석 최적화)
- **압축**: Snappy/GZIP

---

## 🏗️ 시스템 내 역할

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code                            │
├─────────────────────────────────────────────────────────────┤
│ Telegram MCP │  DB MCP  │ Analysis MCP │ Portfolio MCP   │
│ (데이터 수집)  │ (저장)    │  (분석)       │   (의사결정)     │
├─────────────────────────────────────────────────────────────┤
│ Parquet Files │   DB     │   Analytics   │   Decisions    │
└─────────────────────────────────────────────────────────────┘
```

### 데이터 플로우
```
Telegram Channels → Telegram MCP → Parquet Files → DB MCP → Database → ...
```

**Telegram MCP의 역할**: 오직 1단계 (데이터 수집 → Parquet 저장)만 담당

---

## 📁 프로젝트 구조

```
telegram-mcp-server/
├── CLAUDE.md                          # 이 가이드 문서
├── README.md                          # 설치 및 실행 가이드
├── pyproject.toml                     # uv 의존성 관리
├── Dockerfile                        # Docker 이미지
├── docker-compose.yml                # 운영 배포용
├── src/
│   ├── telegram_mcp/
│   │   ├── server.py                 # MCP over SSE 서버 메인
│   │   ├── telegram_client.py        # 텔레그램 API 클라이언트
│   │   ├── message_collector.py      # 메시지 수집
│   │   ├── parquet_storage.py        # Parquet 파일 저장
│   │   ├── mcp_tools.py              # MCP 도구 구현
│   │   └── utils.py                  # 유틸리티
│   └── main.py                       # 진입점
├── config/
│   └── channels.yaml                 # 모니터링 채널 목록 (정적 설정)
├── data/                             # Parquet 데이터 저장소
│   ├── messages/                     # 메시지 데이터
│   ├── media/                        # 미디어 파일
│   └── metadata/                     # 런타임 메타데이터 (Parquet)
├── tests/
└── .env.example                      # 환경변수 예시
```

---

## 🔧 MCP 도구 (Tools) 명세

### 연결 관리
- `connect()` - 텔레그램 클라이언트 연결
- `disconnect()` - 연결 해제
- `get_connection_status()` - 연결 상태 확인

### 메시지 수집
- `start_monitoring()` - 실시간 모니터링 시작
- `stop_monitoring()` - 모니터링 중지
- `collect_messages(channel, start_time, end_time, limit)` - 절대 시간 기준 배치 수집

### 기본 상태 조회
- `get_monitored_channels()` - 설정된 채널 목록 확인
- `get_collection_status()` - 현재 수집 상태 확인

---

## 📄 Parquet 데이터 스키마

### 메시지 테이블 스키마
```python
messages_schema = {
    'message_id': 'int64',
    'channel_username': 'string',
    'channel_title': 'string', 
    'text': 'string',
    'timestamp': 'timestamp[us]',
    'sender_user_id': 'int64',
    'sender_username': 'string',
    'sender_first_name': 'string',
    'forward_from_channel': 'string',
    'forward_original_date': 'timestamp[us]',
    'reply_to_message_id': 'int64',
    'media_type': 'string',
    'media_file_path': 'string',
    'collected_at': 'timestamp[us]',
    'collection_batch_id': 'string'
}
```

### 채널 메타데이터 스키마
```python
channels_schema = {
    'channel_username': 'string',
    'channel_title': 'string',
    'channel_id': 'int64',
    'participants_count': 'int64',
    'description': 'string',
    'is_verified': 'bool',
    'last_updated': 'timestamp[us]',
    'monitoring_status': 'string'
}
```

---

## 🗂️ 파일 저장 구조

### Parquet 파티셔닝 전략 (Hive 스타일)
```
data/
├── messages/
│   ├── year=2025/
│   │   ├── month=09/
│   │   │   ├── day=13/
│   │   │   │   ├── hour=10/
│   │   │   │   │   ├── channel=insidertracking/
│   │   │   │   │   │   └── batch_001.parquet
│   │   │   │   │   └── channel=cryptonews/
│   │   │   │   │       └── batch_001.parquet
│   │   │   │   └── hour=11/
│   │   │   └── day=14/
│   │   └── month=10/
│   └── year=2026/
├── media/
│   ├── year=2025/month=09/day=13/    # 미디어도 동일한 파티셔닝
│   │   ├── images/
│   │   ├── videos/
│   │   └── documents/
│   └── year=2025/month=09/day=14/
└── metadata/
    ├── channels.yaml                 # 정적 설정 (YAML)
    ├── collection_batches.parquet    # 런타임 로그 (Parquet)
    └── system_stats.parquet          # 런타임 통계 (Parquet)
```

### 배치 처리 전략
- **배치 크기**: 10,000개 메시지 또는 1시간 단위
- **시간 기준**: UTC 절대 시간 (start_time, end_time)
- **압축**: Snappy (속도 우선) 또는 GZIP (용량 우선)
- **파티셔닝**: year/month/day/hour/channel 별 Hive 스타일
- **인덱싱**: 타임스탬프 기준 자동 정렬

---

## 🛠️ 설치 및 설정

### 필수 요구사항
1. Python 3.12+
2. uv 패키지 매니저
3. 텔레그램 API 키 (api_id, api_hash)
4. 충분한 디스크 공간 (Parquet 파일 저장용)

### 의존성 설치
```bash
# 프로젝트 초기화
uv sync

# 주요 패키지 확인
# - fastapi (SSE 엔드포인트)
# - uvicorn (ASGI 서버)
# - mcp (Model Context Protocol)
# - telethon (텔레그램 API)
# - pyarrow (Parquet 처리)
# - pandas (데이터 처리)
# - asyncio (비동기 처리)
```

### 환경 설정
```bash
# 환경변수 설정
cp .env.example .env

# 필수 환경변수
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_SESSION=mcp_session

# Parquet 설정
PARQUET_COMPRESSION=snappy
PARQUET_BATCH_SIZE=10000
PARQUET_WRITE_BATCH_SIZE=1000

# 데이터 디렉토리 생성
mkdir -p data/{messages,media,metadata}
```

### Claude Code 연결 (MCP over SSE)
```json
{
  "mcpServers": {
    "telegram-mcp": {
      "transport": "sse",
      "url": "http://localhost:8080/sse"
    }
  }
}
```

### MCP 서버 실행
```bash
# Docker 컨테이너로 MCP 서버 실행
docker-compose up -d telegram-mcp

# 헬스체크
curl http://localhost:8080/health

# SSE 엔드포인트 확인
curl http://localhost:8080/sse

# Claude Code에서 MCP 도구 사용
claude-code run "텔레그램에 연결해줘"
```

---

## 🚀 사용법

### 기본 워크플로우
```bash
# 1. Docker MCP 서버 실행
docker-compose up -d telegram-mcp

# 2. Claude Code를 통한 MCP 도구 사용
claude-code run "텔레그램에 연결해줘"

# 3. 실시간 모니터링 시작 (channels.yaml 기준)
claude-code run "모니터링을 시작해줘"

# 4. 절대 시간 기준 배치 수집
claude-code run "insidertracking 채널의 2025-09-13 00:00:00부터 2025-09-13 23:59:59까지 메시지를 수집해줘"

# 5. 수집 상태 확인
claude-code run "현재 수집 상태를 보여줘"

# 6. 모니터링 중지
claude-code run "모니터링을 중지해줘"
```

### 채널 설정 (channels.yaml)
```yaml
channels:
  - username: "insidertracking"
    priority: "high"
    media_download: true
  - username: "cryptonews" 
    priority: "medium"
    media_download: false
  - username: "financedata"
    priority: "low"
    media_download: false

settings:
  batch_interval_minutes: 60
  max_messages_per_batch: 10000
  media_size_limit_mb: 50
```

---

## 🏗️ 개발 가이드

### 핵심 설계 원칙
1. **단일 책임**: 오직 텔레그램 데이터 수집만
2. **배치 처리**: 효율적인 대용량 데이터 처리
3. **파티셔닝**: 날짜/채널 기준 데이터 분할
4. **압축 최적화**: 저장 공간 및 I/O 효율성

### 주요 컴포넌트
- **MCP over SSE Server**: FastAPI 기반 SSE 엔드포인트 제공
- **TelegramClient**: Telethon 기반 비동기 클라이언트
- **MessageCollector**: 배치 단위 메시지 수집
- **ParquetStorage**: PyArrow 기반 Parquet 저장
- **BatchScheduler**: 시간 기반 배치 스케줄링

### 성능 최적화
- **스트리밍 처리**: 메모리 효율적인 배치 처리
- **컬럼형 압축**: Parquet 스키마 최적화
- **파티션 pruning**: 쿼리 시 불필요한 파일 스킵
- **인덱스 활용**: 타임스탬프 기준 정렬 유지

---

## 🐳 Docker 배포

### 기본 실행
```bash
# 빌드 및 실행
docker-compose up -d

# 로그 모니터링
docker-compose logs -f telegram-mcp

# 데이터 볼륨 확인
docker volume ls | grep telegram
```

### 볼륨 마운트
```yaml
volumes:
  - ./data/messages:/app/data/messages      # Parquet 메시지 파일
  - ./data/media:/app/data/media            # 미디어 파일
  - ./data/metadata:/app/data/metadata      # 메타데이터
  - ./sessions:/app/sessions                # 텔레그램 세션
  - ./config:/app/config                    # 설정 파일
```

### 환경변수
```bash
# 텔레그램 API
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
TELEGRAM_SESSION=mcp_session

# Parquet 설정
PARQUET_COMPRESSION=snappy
PARQUET_ENGINE=pyarrow
PARQUET_BATCH_SIZE=10000
PARQUET_ROW_GROUP_SIZE=100000

# 배치 설정
BATCH_INTERVAL_MINUTES=60
MAX_MESSAGES_PER_BATCH=10000
ENABLE_MEDIA_DOWNLOAD=true
MEDIA_SIZE_LIMIT_MB=50

# 정리 설정
CLEANUP_OLD_FILES_DAYS=30
COMPRESS_OLD_FILES_DAYS=7
```

---

## 📊 모니터링 및 운영

### Parquet 파일 통계
- 일일/시간별 파일 크기 및 압축률
- 채널별 메시지 수집량
- 배치 처리 성능 지표
- 파티션별 쿼리 성능

### 시스템 모니터링
- 텔레그램 연결 상태
- 디스크 I/O 성능
- 메모리 사용 패턴
- Parquet 압축 효율

### 자동화된 정리
- 오래된 파일 압축 (GZIP → LZ4)
- 빈 파티션 정리
- 메타데이터 최적화
- 인덱스 재구성

---

## 🔒 보안 및 제한사항

### 데이터 품질 보증
- Parquet 스키마 검증
- 중복 메시지 제거
- 타임스탬프 정렬 보장
- 배치 무결성 검사

### API 효율성
- 텔레그램 Rate Limit 최적화
- 배치 단위 요청 처리
- 지수 백오프 재시도
- 연결 풀링

---

## 🚀 로드맵

### Phase 1: Parquet 기반 구축 (1주)
- [x] MCP over SSE 서버 기본 구조
- [ ] 텔레그램 클라이언트 연동
- [ ] Parquet 저장 시스템
- [ ] 배치 스케줄러
- [ ] 미디어 파일 다운로드

### Phase 2: 성능 최적화 (1주)  
- [ ] 파티셔닝 전략 구현
- [ ] 압축 알고리즘 최적화
- [ ] 메모리 효율성 개선
- [ ] 쿼리 성능 벤치마킹
- [ ] 자동 정리 시스템

### Phase 3: 운영 안정성 (1주)
- [ ] 대용량 채널 처리 최적화
- [ ] 장애 복구 메커니즘
- [ ] 모니터링 대시보드
- [ ] 성능 프로파일링
- [ ] 문서화 완성

---

## 📞 지원

- **GitHub Issues**: 버그 리포트 및 기능 요청
- **Documentation**: MCP 도구 문서 및 설치 가이드
- **Performance**: Parquet 최적화 가이드

---

## 📜 라이선스

MIT License

**면책사항**: 공개 채널의 공개 메시지만 수집하며, 수집된 데이터는 정보 제공 목적으로만 사용됩니다. 사용자는 관련 법규 및 텔레그램 이용약관을 준수할 책임이 있습니다.

---

*Version: 2.0.0 (MCP over SSE + Parquet Optimized)*  
*Last Updated: 2025-09-14*
