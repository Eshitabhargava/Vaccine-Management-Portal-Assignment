"""
Controller for performing following operations: 
    1. Modifying Vaccination details
    2. Fetching vaccination data for a single user
    3. Fetching vaccination data for multiple users
    4. Filtering data based on: Gender [Male/Female], is_fully_vaccinated, first_doze_taken, second_doze_taken
"""
# Builtin imports
from flask_restx import Namespace, Resource, fields

# Custom imports
from service.account import (
    modify,
    fetch_object,
    fetch_accounts,
    delete,
)
from utils.decorators import decode_auth_token
from utils.validator import validate_params

vaccination_ns = Namespace("vaccines")

vaccination_details_model = vaccination_ns.model(
    "VaccinationDataController",
    {
        "first_doze_taken": fields.String(),
        "first_doze_date": fields.Date(),
        "second_doze_taken": fields.String(),
        "second_doze_date": fields.Date(),
        "is_fully_vaccinated": fields.String(),
    }
)

vaccine_data_filter_model = vaccination_ns.model(
    "RetrievalController",
    {
        "filter": fields.String(), 
        "auth": fields.String(), 
    },
)


@vaccination_ns.route("/<int:ac_id>")
class VaccinationDataController(Resource):
    @vaccination_ns.expect(vaccination_details_model, validate=False)
    @validate_params(vaccination_details_model)
    @decode_auth_token
    def put(self, ac_id: int, **kwargs):
        """
        Modify vaccination details for the given user account
        """
        response = modify(account_id=ac_id, details=kwargs)
        return response

    @decode_auth_token
    def get(self, *args, **kwargs):
        """
        Fetch vaccination data for a single user account
        """
        kwargs["vaccine_data"] = True
        response = fetch_object(kwargs)
        return response


@vaccination_ns.route("")
class RetrievalController(Resource):
    @vaccination_ns.expect(vaccine_data_filter_model, validate=False)
    @validate_params(vaccine_data_filter_model)
    @decode_auth_token
    def get(self, *args, **kwargs):
        """
        Fetch list of users' vaccination data 
        """
        response = fetch_accounts(kwargs)
        return response