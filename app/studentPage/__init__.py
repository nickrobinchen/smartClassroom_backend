from flask import Blueprint

studentPage = Blueprint('studentPage', __name__)

from . import studentList
from . import klassInfo
from . import addStudent
from . import deleteStudent
from . import editStudent