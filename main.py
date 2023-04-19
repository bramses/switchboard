from fastapi import Depends, FastAPI, Security
import auth
from fastapi.security.api_key import APIKey

from fastapi.openapi.utils import get_openapi
import json

app = FastAPI()

@app.get("/secure")
async def info(api_key: APIKey = Depends(auth.get_api_key)):
    return {
        "default variable": api_key
    }

@app.get("/") 
async def main_route():     
  return {"message": "switchboard"}

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


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    file = open("./.well-known/ai-plugin.json", "r")
    return json.load(file)

app.openapi = custom_openapi