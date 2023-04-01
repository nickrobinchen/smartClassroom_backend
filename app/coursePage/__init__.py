from flask import Blueprint

coursePage = Blueprint('coursePage', __name__)

from . import courseList
from . import addCourse
from . import deleteCourse
from . import editCourse