from fastapi import Depends, FastAPI, Response
import auth
from fastapi.security.api_key import APIKey
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "https://chat.openai.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/secure")
async def info(api_key: APIKey = Depends(auth.get_api_key)):
    return {
        "default variable": api_key
    }

@app.get("/todo-list", description="Get a list of todos", tags=["todos"])
async def todo_list(api_key: APIKey = Depends(auth.get_api_key)):
    print(api_key)
    todos = [
        {
            "id": 1,
            "title": "Todo 1",
            "description": "Todo 1 description"
        },
        {
            "id": 2,
            "title": "Todo 2",
            "description": "Todo 2 description"
        }
    ]
    
    return {
        "todos": todos
    }


@app.get("/", description="homepage list of routes", tags=["homepage"]) 
async def main_route():   
  html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>switchboard</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
                <li><a href="/openapi.json">/openapi.json</a></li>
                <li><a href="/.well-known/ai-plugin.json">/.well-known/ai-plugin.json</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""  
  return HTMLResponse(html)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="switchboard",
        version="3.0.2",
        description="description for switchboard api",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    # if components.schema is not defined add it (for openai error: Error getting system message: {"message":"Could not parse OpenAPI spec for plugin: ['In components section, schemas subsection is not an object']"})
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
        openapi_schema["components"]["schemas"] = {}
    else:
        if "schemas" not in openapi_schema["components"]:
            openapi_schema["components"]["schemas"] = {}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    file = open("./.well-known/ai-plugin.json", "r")
    return Response(content=file.read(), media_type="application/json")

app.openapi = custom_openapi