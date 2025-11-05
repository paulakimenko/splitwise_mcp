"""Pydantic models used by the FastAPI application."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, field_validator


class MCPCallRequest(BaseModel):
    """Request schema for dynamic MCP method calls."""

    args: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments to pass to the underlying Splitwise SDK method",
    )


class AddExpenseEqualSplitRequest(BaseModel):
    group_name: str = Field(..., description="Group name")
    amount: float = Field(..., description="Expense amount")
    currency_code: str = Field(..., description="Three-letter currency code, e.g. UAH")
    participant_name: str = Field(..., description="Name of the other participant")
    description: str = Field(..., description="Expense description")

    @field_validator("currency_code")
    @classmethod
    def currency_upper(cls, v: str) -> str:
        return v.upper()


class MonthlyReportRequest(BaseModel):
    group_name: str
    month: str  # format YYYY-MM


class GenericResponse(BaseModel):
    message: str
    data: Optional[Any] = None
