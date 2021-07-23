import pdb

from flask import Blueprint

ab = Blueprint('loginauth', __name__)

from app.auth import view