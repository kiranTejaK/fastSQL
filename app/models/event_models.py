# app/models/event_models.py
import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
 
class GetEventDetailsRequest(BaseModel):
    event_id: int = Field(..., gt=0,  error_msg="event_id must be a positive integer")
 
# class EventCreateRequest(BaseModel):
#     # Mandatory fields
#     event_name_ar: str = Field(..., min_length=2, error_msg="event_name_ar must be at least 2 characters long")
#     event_desc_ar: str = Field(..., min_length=2, error_msg="event_desc_ar must be at least 2 characters long")
#     status: int = Field(..., ge=0, le=1, error_msg="status must be either 0 or 1")
#     event_datetime: str = Field(..., error_msg="event_datetime cannot be empty")
#     event_image: int = Field(..., gt=0, error_msg="event_image must be a positive integer")
#     event_sort_rank: int = Field(..., ge=0, error_msg="event_sort_rank must be a non-negative integer")
 
#     # Optional fields
#     event_name_en: Optional[str] = Field(None, min_length=2, error_msg="event_name_en must be at least 2 characters long if provided")
#     event_desc_en: Optional[str] = Field(None, min_length=2, error_msg="event_desc_en must be at least 2 characters long if provided")
from pydantic import BaseModel, Field, validator
from typing import Optional
 
class EventCreateRequest(BaseModel):
    # Mandatory fields
    event_name_ar: str = Field(..., min_length=2)
    event_desc_ar: str = Field(..., min_length=2)
    status: int = Field(..., ge=0, le=1)
    event_datetime: str
    event_image: int = Field(..., gt=0)
    event_sort_rank: int = Field(..., ge=0)
   
    # Optional fields
    event_name_en: Optional[str] = Field(None, min_length=2)
    event_desc_en: Optional[str] = Field(None, min_length=2)
 
    # Custom validators with specific error messages
    @field_validator('event_name_ar', 'event_desc_ar', 'event_name_en', 'event_desc_en')
    def validate_min_length(cls, v, field):
        if v is not None and len(v) < 2:
            raise ValueError(f"{field.name} must be at least 2 characters long")
        return v
 
    @field_validator('status')
    def validate_status(cls, v):
        if v not in (0, 1):
            raise ValueError("status must be either 0 or 1")
        return v
 
    @field_validator('event_image')
    def validate_event_image(cls, v):
        if v <= 0:
            raise ValueError("event_image must be a positive integer")
        return v
 
    @field_validator('event_sort_rank')
    def validate_event_sort_rank(cls, v):
        if v < 0:
            raise ValueError("event_sort_rank must be a non-negative integer")
        return v
   
    @field_validator('event_datetime')
    def validate_event_datetime(cls, v):
        # List of valid formats
        formats = [
            "%Y-%m-%d %H:%M:%S",  # 2024-01-21 15:30:00
            "%Y-%m-%d"            # 2024-01-21
        ]
 
        for fmt in formats:
            try:
                datetime.strptime(v, fmt)
                return v
            except ValueError:
                continue
       
        raise ValueError("Invalid datetime format. Must be either 'YYYY-MM-DD HH:MM:SS' or 'YYYY-MM-DD'")
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
    