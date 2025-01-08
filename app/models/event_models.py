# app/models/event_models.py
from pydantic import BaseModel, Field
from typing import Optional

class GetEventDetailsRequest(BaseModel):
    event_id: int = Field(..., gt=0,  error_msg="event_id must be a positive integer")

class EventCreateRequest(BaseModel):
    # Mandatory fields
    event_name_ar: str = Field(..., min_length=2, error_msg="event_name_ar must be at least 2 characters long")
    event_desc_ar: str = Field(..., min_length=2, error_msg="event_desc_ar must be at least 2 characters long")
    status: int = Field(..., ge=0, le=1, error_msg="status must be either 0 or 1")
    event_datetime: str = Field(..., error_msg="event_datetime cannot be empty")
    event_image: int = Field(..., gt=0, error_msg="event_image must be a positive integer")
    event_sort_rank: int = Field(..., ge=0, error_msg="event_sort_rank must be a non-negative integer")

    # Optional fields
    event_name_en: Optional[str] = Field(None, min_length=2, error_msg="event_name_en must be at least 2 characters long if provided")
    event_desc_en: Optional[str] = Field(None, min_length=2, error_msg="event_desc_en must be at least 2 characters long if provided")

class EventUpdateRequest(BaseModel):
    # Mandatory fields
    event_id: int = Field(..., gt=0,  error_msg="event_id must be a positive integer")
    event_name_ar: str = Field(..., min_length=2, error_msg="event_name_ar must be at least 2 characters long")
    event_desc_ar: str = Field(..., min_length=2, error_msg="event_desc_ar must be at least 2 characters long")
    status: int = Field(..., ge=0, le=1, error_msg="status must be either 0 or 1")
    event_datetime: str = Field(..., error_msg="event_datetime cannot be empty")
    event_image: int = Field(..., gt=0, error_msg="event_image must be a positive integer")
    event_sort_rank: int = Field(..., ge=0, error_msg="event_sort_rank must be a non-negative integer")

    # Optional fields
    event_name_en: Optional[str] = Field(None, min_length=2, error_msg="event_name_en must be at least 2 characters long if provided")
    event_desc_en: Optional[str] = Field(None, min_length=2, error_msg="event_desc_en must be at least 2 characters long if provided")
