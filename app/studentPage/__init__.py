from flask import Blueprint

studentPage = Blueprint('studentPage', __name__)

from . import studentList
from . import classInfo
from . import addStudent
from . import deleteStudent
from . import editStudent