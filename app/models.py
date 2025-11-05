"""Pydantic models used by the FastAPI application."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator


class MCPCallRequest(BaseModel):
    """Request schema for dynamic MCP method calls."""

    args: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments to pass to the underlying Splitwise SDK method",
    )


class AddExpenseEqualSplitRequest(BaseModel):
    group_name: str = Field(..., description="Назва групи")
    amount: float = Field(..., description="Сума витрати")
    currency_code: str = Field(..., description="Тривсимвольний код валюти, напр. UAH")
    participant_name: str = Field(..., description="Ім'я іншого учасника")
    description: str = Field(..., description="Коментар до витрати")

    @validator("currency_code")
    def currency_upper(cls, v: str) -> str:  # noqa: N805
        return v.upper()


class MonthlyReportRequest(BaseModel):
    group_name: str
    month: str  # format YYYY-MM


class GenericResponse(BaseModel):
    message: str
    data: Optional[Any] = None
