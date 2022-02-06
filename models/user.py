import datetime
import json
import uuid

import glog as log
import jwt
from flask import jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
from constants import db


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String())
    account_type = db.Column(db.String())
    vaccine_name = db.Column(db.String())
    first_doze_taken = db.Column(db.String()) 
    first_doze_date = db.Column(db.DateTime)
    second_doze_taken = db.Column(db.String())
    second_doze_date = db.Column(db.DateTime) 
    is_fully_vaccinated = db.Column(db.String())

    def __init__(self, user_data=None):
        if not user_data:
            user_data = {}
        self.email = user_data.get("email")
        self.name = user_data.get("name")
        self.gender = user_data.get("gender")
        self.age = user_data.get("age") 
        self.phone_number = user_data.get("phone_number")
        self.vaccine_name = user_data.get("vaccine_name")
        self.first_doze_taken = user_data.get("first_doze_taken")
        self.first_doze_date = user_data.get("first_doze_date")
        self.second_doze_taken = user_data.get("second_doze_taken")
        self.second_doze_date = user_data.get("second_doze_date")
        self.is_fully_vaccinated = user_data.get("is_fully_vaccinated")
        if user_data.get("password"):
            self.password = Bcrypt().generate_password_hash(user_data.get("password")).decode()

    def to_response_dict(self):
        """
        Helps json-ify the user object for sending to FE.
        """
        resp_dict = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "phone_number": self.phone_number,
            "vaccine_name": self.vaccine_name,
            "first_doze_taken": self.first_doze_taken,
            "first_doze_date": self.first_doze_date,
            "second_doze_taken": self.second_doze_taken,
            "second_doze_date": self.second_doze_date,
            "is_fully_vaccinated": self.is_fully_vaccinated
        }
        return resp_dict

    @staticmethod
    def fetch_user(params):
        """
        Fetches user data from database based on provided params
        """
        try:
            user_object = db.session.query(User).filter_by(**params).first()
            if user_object:
                return user_object
        except Exception as e:
            log.info(e, exc_info=True)
            return False

    @staticmethod
    def generate_auth_token(email_id):
        """
        Generates the Auth Token
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2, seconds=0),
                "iat": datetime.datetime.utcnow(),
                "sub": email_id,
            }
            return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
        except Exception as e:
            log.info(e)

    def create(self):
        """
        Saves the object data to DB and populates ids and dates.
        """
        db.session.add(self)
        db.session.flush()
        db.session.commit()

    def update(self, filter_param, update_params):
        """
        Updates the object data to DB.
        """
        db.session.query(self.__class__).filter_by(**filter_param).update(update_params)
        db.session.commit()

    def delete(self, filter_param):
        """
        Sets status of object as False in DB
        """
        db.session.query(self.__class__).filter_by(**filter_param).update({"deleted_at": self.deleted_at})
        db.session.commit()

    @staticmethod
    def find_by_email(email):
        """
        Returns user object from DB using email
        """
        try:
            user_obj = User.query.filter_by(email=email).first()
            if user_obj:
                return user_obj
            return False
        except Exception as e:
            log.info(e, exc_info=True)
            return False
