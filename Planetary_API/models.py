from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean
import os
from app import db

class User(db.model):
    __tablename__ = "users" # This controls the name of the table
    id = Column(Integer, primary_key=True) # These are the instance variables that are created/ treated as columns in an actual table
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    username = Column(String, unique=True)


class Planet(db.model):
    __tablename__ = "planets"
    planet_id = Column(Integer, primary_key = True)
    planet_name = Column(String)
    planet_star = Column(String)
    is_inhabitable = Column(Boolean)
    radius = Column(Float)
    mass = Column(Float)
    population = Column(Float)
    