"""
Controller for performing following operations: 
    1. Registering a new user
    2. Logging into existing user accounts
    3. CRUD operations on user accounts
"""
# Builtin imports
from flask_restx import Namespace, Resource, fields

# Custom imports
from service.account import (
    register,
    authenticate,
    modify,
    fetch_object,
    delete,
)
from utils.decorators import decode_auth_token
from utils.validator import validate_params

account_ns = Namespace("account")


# Models for input data
account_register_model = account_ns.model(
    "RegisterController",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
        "name": fields.String(required=True),
        "gender": fields.String(required=True),
        "age": fields.Integer(required=True),
        "phone_number": fields.String(required=True),
        "account_type": fields.String(required=True),
    },
)

account_login_model = account_ns.model(
    "LoginController",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    }
)

account_modify_model = account_ns.model(
    "ModifyController",
    {
        "updated_email": fields.String(),
        "password": fields.String(),
        "name": fields.String(),
        "account_type": fields.String(),
        "gender": fields.String(),
        "age": fields.Integer(),
        "phone_number": fields.String(),
    },
)

account_filter = account_ns.model(
    "FilterController",
    {
        "filter": fields.String(), 
        "auth": fields.String()
    },
)

delete_account_model = account_ns.model(
    "DeleteController",
    {
        "email": fields.String(),
    },
)


@account_ns.route("/register")
class RegistrationController(Resource):
    @account_ns.expect(account_register_model, validate=False)
    @validate_params(account_register_model)
    def post(self, *args, **kwargs):
        """
        Registers a new account with a unique email.
        """
        response = register(details=kwargs.get("params"))
        return response


@account_ns.route("/login")
class LoginController(Resource):
    @account_ns.expect(account_login_model, validate=False)
    @validate_params(account_login_model)
    def post(self, *args, **kwargs):
        """
        Login the user with email and password coming encrypted from FE.
        """
        response = authenticate(kwargs)
        return response


@account_ns.route("/<int:ac_id>")
class ModificationController(Resource):
    @account_ns.expect(account_modify_model, validate=False)
    @validate_params(account_modify_model)
    @decode_auth_token
    def put(self, ac_id: int, **kwargs):
        """
        Modify general account details
        """
        response = modify(account_id=ac_id, details=kwargs)
        return response

    @account_ns.expect(account_modify_model, validate=False)
    @validate_params(account_modify_model)
    @decode_auth_token
    def delete(self, ac_id, **kwargs):
        """
        Delete user account
        """
        response = delete(account_id=ac_id, details=kwargs)
        return response

    @account_ns.expect(account_filter, validate=False)
    @validate_params(account_filter)
    @decode_auth_token
    def get(self, *args, **kwargs):
        """
        Fetch the account details
        """
        response = fetch_object(params={"id":kwargs.get("id")})
        return response