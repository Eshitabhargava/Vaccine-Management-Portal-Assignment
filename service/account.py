# Standard imports
from flask import Response
import logging as log
import json
from datetime import datetime, timedelta
from constants import BASE_HEADERS, bcrypt

# Custom imports
from models.user import User
from constants import EMAIL_REGEX, bcrypt
from utils.exceptions import (
    InvalidEmailError,
    UserAlreadyExistsError,
    UserUnauthorizedError,
    ParameterError,
    NotFoundError
)

def _valid_password(user_object, provided_password):
    """
    Checks user creds and tells if user can login or not
    """
    return bool(bcrypt.check_password_hash(user_object.password, provided_password))

def register(details):
    """
    Registers new user to our app
    """
    fetched_admin, fetched_email = [], []
    if not EMAIL_REGEX.fullmatch(details.get("email", "")):
        log.warning("The entered email is invalid - {}".format(details.get("email")))
        raise InvalidEmailError
    if details.get("account_type") == "admin":
        fetched_admin = User().fetch_user({"account_type": "admin"})
    fetched_email = User.find_by_email(email=details.get("email"))
    if fetched_admin or fetched_email:
        log.warning("User already exists - {}".format(details.get("email")))
        raise UserAlreadyExistsError
    else:
        User(user_data=details).create()
        response = Response(
                response=json.dumps(obj={"message":"User - {} Registered Successfully".format(details.get("email"))}),
                status=200,
                mimetype="application/json"
            )
    return response


def authenticate(details):
    """
    Authenticates user and generates a auth key
    """
    post_data = details.get("params")
    if not EMAIL_REGEX.fullmatch(post_data.get("email")):
        log.warning("The entered email is invalid {}".format(post_data.get("email")))
        raise InvalidEmailError
    user_obj = User.find_by_email(email=post_data.get("email", ""))
    if not user_obj:
        log.warning("User not found - {}".format(post_data.get("email")))
        raise AuthError()
    if not _valid_password(
        user_object=user_obj, provided_password=post_data.get("password")
    ):
        log.warning("Auth Failed, Valid username/password required - {}".format(post_data.get("password")))
        raise AuthError()
    auth_token = user_obj.generate_auth_token(user_obj.email)
    if not auth_token:
        log.warning("Cannot generate Auth Token")
        raise AuthTokenGenError()
    data = {"auth_token": auth_token, "message": "authentication successful"}
    response = Response(
                response=json.dumps(obj=data),
                status=200,
                mimetype="application/json"
            )
    return response


def modify(account_id, details):
    """
    Modifies the user account details
    """
    post_data = details.get("params")
    if not post_data:
        raise ParameterError("No data to update")

    current_email = details.get("email")
    fetched_content = User.find_by_email(email=current_email)
    if not fetched_content:
        log.warning("User not found {}".format(current_email))
        return NotFoundError()

    if "updated_email" in post_data:
        if not EMAIL_REGEX.fullmatch(post_data.get("updated_email")):
            log.warning(
                "The entered email is invalid {}".format(post_data.get("updated_email"))
            )
            raise InvalidEmailError
        post_data["email"] = post_data.get("updated_email")

    if "password" in post_data:
        post_data["password"] = bcrypt.generate_password_hash(
                post_data.get("password")
            ).decode()
    # will restrict user but not admin
    if details.get("account_type") != "admin":
        account_id = details.get("id")
    User().update(filter_param={"id": account_id}, update_params=post_data)
    response = Response(
                response=json.dumps(obj={"message":"User Details modified successfully"}),
                status=200,
                mimetype="application/json"
            )
    return response


def fetch_accounts(request_details):
    """
    Fetches user accounts based on multiple filter or filters
    """
    if request_details.get("account_type") != "admin":
        return UserUnauthorizedError()
    _filter = {}
    fetch_all = False
    if request_details.get("params").get("filter") == "all":
        fetch_all = True
        details = {}
    else:
        details = {request_details.get("params").get("filter"): request_details.get("params").get("value")}
    if request_details.get("params", {}).pop("auth", False) in ("True", "true"):
        _filter["email"] = request_details.get("email")
    elif request_details.get("account_type") != "admin" and request_details.get("params"):
        _filter["email"] = request_details.get("email")
        _filter.update(details)
    elif request_details.get("account_type") == "admin" and request_details.get("params"):
        _filter.update(details)
    else:
        raise ParameterError(message="filter or auth param required")
    if fetch_all:
        data = User().fetch_all({"filter": "all"})
    else:
        data = User().fetch_all(params=_filter)
    if not data:
        log.warning("User not found".format(_filter))
        return NotFoundError()
    resp_data = []
    for d in data:
        resp_data.append(d.to_response_dict())
    response = Response(
            response=json.dumps(obj=resp_data),
            status=200,
            mimetype="application/json"
        )
    return response


def fetch_object(kwargs):
    """
    returns object of queried param
    """
    params = {"id":kwargs.get("id")}
    data = User().fetch_user(params).to_response_dict()
    vaccine_data = kwargs.get("vaccine_data", False)
    if not vaccine_data:
        data.pop("vaccine_name")
        data.pop("first_doze_taken")
        data.pop("first_doze_date")
        data.pop("second_doze_taken")
        data.pop("second_doze_date")
        data.pop("is_fully_vaccinated")
    return data


def delete(account_id, details):
    """
    Deletes user account
    """
    if details.get("account_type") != "admin":
        account_id = details.get("id")

    user_arr = User().fetch_by_id(params={"id": account_id})
    if not user_arr:
        log.warning("user does not exist")
        return NotFoundError()

    user_obj = User.find_by_email(user_arr[0].get("email"))
    user_obj.delete()
    response = Response(
                response=json.dumps(obj={"message":"User Deleted successfully"}),
                status=200,
                mimetype="application/json"
            )
    return response

