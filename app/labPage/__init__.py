from flask import Blueprint

labPage = Blueprint('labPage', __name__)

from . import labList
from . import addLab
from . import editLab
from . import deleteLab
