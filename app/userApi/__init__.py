from flask import Blueprint

userPage = Blueprint('userApi', __name__)

from . import login
from . import logout