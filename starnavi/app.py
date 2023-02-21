from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starnavi.utils.settings import Settings
from social_network.routers import user_router, post_router
from social_network.middleware import   LastRequestMiddleware
from social_network import models
from social_network.database import engine


app = FastAPI()
settings = Settings()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(LastRequestMiddleware)

@app.get("/")
async def root():
    """Base route, id is some useful links right here"""
    html_content = """
        <head>
    <html>
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


app.include_router(user_router, prefix="/api")
app.include_router(post_router, prefix="/api")