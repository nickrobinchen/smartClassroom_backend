from flask import Blueprint

studentPage = Blueprint('studentApi', __name__)

from . import studentList
from . import classInfo
from . import addStudent
from . import deleteStudent
from . import editStudent