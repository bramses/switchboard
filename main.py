
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# from https://fastapi.tiangolo.com/tutorial/security/first-steps/#__tabbed_1_1 (nyi)
# and https://medium.com/@caetanoog/start-your-first-fastapi-server-with-poetry-in-10-minutes-fef90e9604d9
@app.get("/items/", description="Get items from the database")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# @app.get("/") 
# async def main_route():     
#   return {"message": "Hey, It is me Goku"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi