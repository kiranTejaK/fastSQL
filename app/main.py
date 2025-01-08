# app/main.py
from fastapi import FastAPI
from app.routes.event_routes import router as event_router
from app.exceptions.response_exceptions import internal_server_error_handler, bad_request_error_handler, validation_exception_handler, InternalServerError, BadRequestError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import HTTPException

app = FastAPI()

# Register custom exception handlers
app.add_exception_handler(HTTPException, internal_server_error_handler)  # Global handler for all HTTPException (including custom ones)
app.add_exception_handler(InternalServerError, internal_server_error_handler)
app.add_exception_handler(BadRequestError, bad_request_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Include routes
app.include_router(event_router)


