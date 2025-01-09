# app/exceptions/response_exceptions.py
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse # type: ignore

# Custom exception class for internal server errors
class InternalServerError(HTTPException):
    def __init__(self, detail: str):
        self.status_code = 500
        self.detail = detail

# Exception handler for InternalServerError
async def internal_server_error_handler(request, exc: InternalServerError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "status_code": "XC500", "status_message": "Internal Server Error", "error_details": exc.detail}
    )

# Custom exception class for bad requests (e.g., missing headers)
class BadRequestError(HTTPException):
    def __init__(self, detail: str):
        self.status_code = 400
        self.detail = detail

# Exception handler for BadRequestError
async def bad_request_error_handler(request, exc: BadRequestError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "status_code": "XC400", "status_message": exc.detail}
    )
    
# Exception handler for RequestValidationError
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for Pydantic validation errors.
    """
    error_details = [
        {"field": err['loc'][-1], "message": err['msg']} for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "status": "F",
            "status_code": "XC400",
            "status_message": "Validation error occurred",
            "http_code": 422,
            "error_details": error_details,
        },
    )
