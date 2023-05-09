from flask import Blueprint

managerPage = Blueprint('managerApi', __name__)

from . import managerInfo