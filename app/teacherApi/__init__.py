from flask import Blueprint

teacherPage = Blueprint('teacherApi', __name__)

from . import teacherList
from . import addTeacher
from . import deleteTeacher
from . import editTeacher
from . import SignIn