from flask import Blueprint

userPage = Blueprint('userPage', __name__)

from . import login
from . import logout