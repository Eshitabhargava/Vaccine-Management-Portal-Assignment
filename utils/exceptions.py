"""
Utils script containing exceptions and handlers for exceptions.
"""
from flask_restx import abort
from flask import Response
from constants import BASE_HEADERS


class InvalidEmailError(Exception):
    """Raise for errors when email syntax is not valid"""

    def __init__(self, message="The entered email is invalid"):
        self.message = message
        super().__init__(self.message)
        return abort(400, error=self.message, success=False)


class ParameterError(Exception):
    """Raise for errors when all params are not specified"""

    def __init__(self, message="Not enough/ Wrong params entered"):
        self.message = message
        super().__init__(self.message)
        return abort(400, error=self.message, success=False)

class UserUnauthorizedError(Exception):
    """Raise for errors when user does not have access"""

    def __init__(self, message="The user is not authorized"):
        self.message = message
        super().__init__(self.message)
        return abort(403, error=self.message, success=False)


class UserAlreadyExistsError(Exception):
    """Raise for errors when user already exists."""

    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)
        return abort(409, error=self.message, success=False)


class AlreadyExistsError(Exception):
    """Raise for errors when publication already exists."""

    def __init__(self, message="Periodical already exists"):
        self.message = message
        super().__init__(self.message)
        return abort(403, error=self.message, success=False)


class ExpiredSignatureError(Exception):
    """Raised when signature has expired"""

    def __init__(self, message="Signature expired, login again"):
        self.message = message
        super(ExpiredSignatureError, self).__init__(self.message)
        return abort(401, error=self.message, success=False)


class NoAuthTokenPresentError(Exception):
    """Raised when token is not present"""

    def __init__(self, message="Auth token required"):
        self.message = message
        super().__init__(self.message)
        return abort(400, error=self.message, success=False)


def NotFoundError():
    """Raise for errors when user not found."""
    return Response(
        status=204,
        headers=BASE_HEADERS,
    )

class AuthError(Exception):
    """Raise for errors when user has been logged out."""

    def __init__(self, message="Auth Failed, Valid username/password required"):
        self.message = message
        super().__init__(self.message)
        return abort(401, error=self.message, success=False)
