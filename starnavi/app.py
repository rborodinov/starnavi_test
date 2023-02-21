from urllib.request import Request

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starnavi.utils.settings import Settings
from sql_app import main as sql_app
from sql_app.middleware import   LastRequestMiddleware
app = FastAPI()
settings = Settings()



app.add_middleware(LastRequestMiddleware)

@app.get("/")
async def root():
    html_content = """
    <html>
        <head>
            <title>Test Project</title>
        </head>
        <body>
            <h2>Starnavi project shows the magic of fastapi.</h2>
           Visit <a href="http://127.0.0.1:8000/docs">Swagger</a> <br>
           and <a href="http://127.0.0.1:8000/redoc">Redocly</a> <br>
           for some <b>OpenAPI</b> sugar.
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


app.include_router(sql_app.router)