from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException, Depends
from starlette.status import HTTP_401_UNAUTHORIZED
from config import Settings, get_settings

api_key_header = APIKeyHeader(name="Authorization", auto_error=False, description="API Key Header (example is 'my file key')")  


async def get_api_key(settings: Settings = Depends(get_settings), api_key_header: str = Security(api_key_header)):
    if "Bearer" in api_key_header:
        api_key_header = api_key_header.replace("Bearer ", "")
    if api_key_header == settings.API_KEY:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Could not validate API KEY"
        )