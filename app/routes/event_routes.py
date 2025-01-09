# app/routes/event_routes.py
from fastapi import APIRouter, HTTPException, Header
from typing import Optional
import json
from fastapi.responses import JSONResponse

from app.database.db_config import get_db_connection
from app.exceptions.response_exceptions import InternalServerError, BadRequestError
from app.models.event_models import GetEventDetailsRequest, EventCreateRequest, EventUpdateRequest

router = APIRouter()

BAD_REQUEST_MESSAGE = "Request Forged. Missing required headers."

@router.get("/db-test/")
def db_conn_test():
    connection = get_db_connection() 
    if connection:
        return JSONResponse(
            status_code=200,
            content={
                "http_code": 200,
                "status_message": "DB connected successfully."
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "http_code": 500,
                "status_message": "DB connection failure."
            }
        )

@router.post("/get/events/")
async def get_all_events(
    x_api_user_id: Optional[str] = Header(None), 
    x_api_token: Optional[str] = Header(None)
):
    # Initialize variables
    user_id = x_api_user_id
    token = x_api_token

    # Check if the necessary headers are provided
    if not user_id or not token:
        raise BadRequestError(detail=BAD_REQUEST_MESSAGE)

    try:
        # Database query
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        prepared_statement = 'CALL xp_per_all_events_get(%s, %s, %s, %s)'
        bind_parameters = (user_id, token, None, 'en')  # Null for auth_device_id, 'en' for i18n
        
        cursor.execute(prepared_statement, bind_parameters)
        
        # Process result
        data = cursor.fetchone()
        
        if data:
            data['status'] = True if data['status'] == 'S' else False
            return_data = data
            if 'secure_data' in return_data:
                del return_data['secure_data']
            if return_data.get('data'):
                return_data['data'] = json.loads(return_data['data'])

            # Return the response with status code from the data
            return JSONResponse(status_code=data['http_code'], content=return_data)

        else:
            raise InternalServerError(detail="No events found in the database.")

    except Exception as e:
        raise InternalServerError(detail=f"Internal Server Error: {str(e)}")
    finally:
        # Ensure the cursor and connection are closed after the operation
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
@router.post("/get/event-details/")
async def get_event_details(
    request: GetEventDetailsRequest, 
    x_api_user_id: Optional[str] = Header(None), 
    x_api_token: Optional[str] = Header(None)
):
    # Initialize variables
    user_id = x_api_user_id
    token = x_api_token
    event_id = None
    err = 0

    # Check for necessary headers
    if not user_id or not token:
        raise BadRequestError(detail=BAD_REQUEST_MESSAGE)
    
    # Retrieving the payload (request body)
    request_data = request

    # Validate event_id
    if isinstance(request_data.event_id, int) and request_data.event_id > 0:
        event_id = request_data.event_id
    else:
        err += 1

    # Check for validation errors
    if err > 0:
        raise BadRequestError(detail= BAD_REQUEST_MESSAGE)

    try:
        # Database query using mysql.connector
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute stored procedure
        prepared_statement = 'CALL xp_per_all_events_get_by_id(%s, %s, %s, %s, %s)'
        bind_parameters = (event_id, user_id, token, None, 'en')  # Null for auth_device_id, 'en' for i18n

        cursor.execute(prepared_statement, bind_parameters)

        # Process result
        data = cursor.fetchone()

        if data:
            data['status'] = True if data['status'] == 'S' else False
            return_data = data
            if 'secure_data' in return_data:
                del return_data['secure_data']
            if return_data.get('data'):
                return_data['data'] = json.loads(return_data['data'])

            # Return the response with the data and status code from the response
            return JSONResponse(status_code=data['http_code'], content=return_data)

        else:
            raise InternalServerError(detail="No event found for the given ID.")

    except Exception as e:
        raise InternalServerError(detail=f"Internal Server Error: {str(e)}")
    finally:
        # Ensure the cursor and connection are closed after the operation
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@router.post("/event/create/")
async def create_event(
    x_api_user_id: Optional[str] = Header(None),
    x_api_token: Optional[str] = Header(None),
    request_data: EventCreateRequest = None
):
    # Initialize variables
    user_id = x_api_user_id
    token = x_api_token

    if not user_id or not token:
        raise HTTPException(status_code=400, detail=BAD_REQUEST_MESSAGE)

    # Validate and process the request data using Pydantic model (done automatically)
    event_name_ar = request_data.event_name_ar
    event_name_en = request_data.event_name_en
    event_desc_ar = request_data.event_desc_ar
    event_desc_en = request_data.event_desc_en
    event_datetime = request_data.event_datetime
    event_image = request_data.event_image
    status = request_data.status
    event_sort_rank = request_data.event_sort_rank

    connection = None
    cursor = None

    try:
        # Database query using mysql.connector
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Prepare SQL statement
        prepared_statement = '''
            CALL xp_per_all_events_create(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        '''
        bind_parameters = (
            event_name_ar, event_name_en, event_desc_ar, event_desc_en, 
            event_datetime, event_image, event_sort_rank, status,
            user_id, token, None, 'en'  # None for auth_device_id, 'en' for i18n
        )

        cursor.execute(prepared_statement, bind_parameters)
        # Commit the transaction to persist changes

        # Fetch result
        data = cursor.fetchone()

        if data:
            data['status'] = True if data['status'] == 'S' else False
            if 'secure_data' in data:
                del data['secure_data']
            if data.get('data'):
                data['data'] = json.loads(data['data'])
            
            # Return the response
            return data
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error: No data returned.")

    except Exception as e:
        raise InternalServerError(detail=f"Internal Server Error: {str(e)}")
    finally:
        # Ensure the cursor and connection are closed after the operation
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@router.post("/event/update/")
async def update_event(
    x_api_user_id: Optional[str] = Header(None),
    x_api_token: Optional[str] = Header(None),
    request_data: EventUpdateRequest = None
):
    # Initialize variables
    user_id = x_api_user_id
    token = x_api_token

    if not user_id or not token:
        raise HTTPException(status_code=400, detail=BAD_REQUEST_MESSAGE)

    # Validate and process the request data using Pydantic model (done automatically)
    event_id = request_data.event_id
    event_name_ar = request_data.event_name_ar
    event_name_en = request_data.event_name_en
    event_desc_ar = request_data.event_desc_ar
    event_desc_en = request_data.event_desc_en
    event_datetime = request_data.event_datetime
    event_image = request_data.event_image
    status = request_data.status
    event_sort_rank = request_data.event_sort_rank

    try:
        # Database query using mysql.connector
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Prepare SQL statement
        prepared_statement = '''
            CALL xp_per_all_events_update(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        '''
        bind_parameters = (
            event_id, event_name_ar, event_name_en, event_desc_ar, event_desc_en, 
            event_datetime, event_image, event_sort_rank, status,
            user_id, token, None, 'en'  # None for auth_device_id, 'en' for i18n
        )

        cursor.execute(prepared_statement, bind_parameters)

        # Fetch result
        data = cursor.fetchone()

        if data:
            data['status'] = True if data['status'] == 'S' else False
            if 'secure_data' in data:
                del data['secure_data']
            if data.get('data'):
                data['data'] = json.loads(data['data'])
            
            # Return the response
            return data
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error: No data returned.")

    except Exception as e:
        raise InternalServerError(detail=f"Internal Server Error: {str(e)}")
    finally:
        # Ensure the cursor and connection are closed after the operation
        if cursor:
            cursor.close()
        if connection:
            connection.close()