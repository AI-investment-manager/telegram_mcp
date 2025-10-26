from datetime import date, datetime
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from src.application.port.input.message import MessageRetrievalUseCase
from src.infrastructure.container import Container

router = APIRouter(prefix="/message", tags=["message"])


class GetMessageResponse(BaseModel):
    """
    최신 메시지 조회 응답
    """

    id: int = Field(description="메시지 ID", example=1)
    message: str = Field(description="메시지", example="Hello, World!")
    ts: datetime = Field(description="메시지 타임스탬프", example="2025-01-01T00:00:00+09:00")
    peer_name: str = Field(description="채널 이름", example="python")
    peer_id: int = Field(description="채널 ID", example=1)


class ErrorResponse(BaseModel):
    """
    에러 응답
    """

    error: str
    message: str

    class Config:
        """
        Config 설정
        """

        json_schema_extra = {
            "example": {
                "error": "MessageNotFoundError",
                "message": "채널의 메시지가 없습니다.",
            }
        }


@router.get(
    "/latest/{channel_id}",
    response_model=GetMessageResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "메시지 또는 채널을 찾을 수 없음",
        },
    },
)
@inject
async def get_latest_message(
    channel_id: str,
    message_retrieval_use_case: Annotated[MessageRetrievalUseCase, Depends(Provide[Container.message_service])],
):
    """
    최신 메시지 조회
    """
    message = await message_retrieval_use_case.get_latest_message(channel_id)
    return GetMessageResponse(**message.to_dict())


@router.get(
    "/date/{channel_id}",
    response_model=list[GetMessageResponse],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "메시지 또는 채널을 찾을 수 없음",
        },
    },
)
@inject
async def get_messages_by_date(
    channel_id: str,
    date: date,
    message_retrieval_use_case: Annotated[MessageRetrievalUseCase, Depends(Provide[Container.message_service])],
):
    """
    특정 날짜의 메시지 조회
    """
    messages = await message_retrieval_use_case.get_messages_by_date(channel_id, date)
    return [GetMessageResponse(**message.to_dict()) for message in messages]


@router.get(
    "/yesterday/{channel_id}",
    response_model=list[GetMessageResponse],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "메시지 또는 채널을 찾을 수 없음",
        },
    },
)
@inject
async def get_yesterday_messages(
    channel_id: str,
    message_retrieval_use_case: Annotated[MessageRetrievalUseCase, Depends(Provide[Container.message_service])],
):
    """
    어제의 메시지 조회
    """
    messages = await message_retrieval_use_case.get_yesterday_messages(channel_id)
    return [GetMessageResponse(**message.to_dict()) for message in messages]
