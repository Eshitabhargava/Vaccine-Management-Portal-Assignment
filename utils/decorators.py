"""
File to store decorators used across application
"""
import functools
import jwt
import os
import json
from flask import request, g, Response
from decorator import decorator
from jwt.exceptions import ExpiredSignatureError

from models.user import User
from utils.exceptions import NoAuthTokenPresentError, UserUnauthorizedError


@decorator
def decode_auth_token(f, is_req=False, *args, **kwargs):
    """
    Decorator for views that require a certain permission of the logged in
    user.
    """
    if "AUTHORIZATION" in request.headers or "auth_token" in request.view_args:
        auth_token = request.headers.get('AUTHORIZATION') or request.view_args.get('auth_token')
        if auth_token:
            try:
                payload = jwt.decode(auth_token, os.getenv("SECRET_KEY"), "HS256")
            except ExpiredSignatureError:
                response = {}
                response["message"] = "Signature expired, login again"
                return Response(
                    response=json.dumps(obj=response),
                    status=400,
                    mimetype="application/json"
                )
            email = payload["sub"]
            user_obj = User.find_by_email(email=email)
            if not user_obj:
                raise UserUnauthorizedError(message="Authentication failed")
            kwargs["id"] = user_obj.id
            kwargs["account_type"] = user_obj.account_type
            kwargs["email"] = email
            g.user_id = user_obj.id
        return f(*args, **kwargs)
    raise NoAuthTokenPresentError