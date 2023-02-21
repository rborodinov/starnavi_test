from social_network.crud import update_user_last_request, get_user_by_email
from social_network.security import get_current_user_email
from sqlalchemy.orm import Session

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.security.utils import get_authorization_scheme_param
from fastapi.responses import JSONResponse, Response


class LastRequestMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        authorization = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if scheme == "Bearer":
            try:
                email = get_current_user_email(token=param)
                from social_network.database import engine
                with Session(engine) as db:
                    user = get_user_by_email(db, email)
                    update_user_last_request(db, user)
            except Exception as e:
                return JSONResponse(content=e.__dict__, status_code=e.__dict__.get('status_code', 500))
            print()

        # process the request and get the response
        response = await call_next(request)

        return response
