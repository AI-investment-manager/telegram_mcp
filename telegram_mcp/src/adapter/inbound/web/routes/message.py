from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from src.application.port.input.message import MessageRetrievalUseCase
from src.infrastructure.container import Container

router = APIRouter(prefix="/message", tags=["message"])


class GetLatestMessageResponse(BaseModel):
    """
    최신 메시지 조회 응답
    """

    message: str = Field(description="메시지", example="Hello, World!")


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
    response_model=GetLatestMessageResponse,
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
    return GetLatestMessageResponse(message=message.message)
