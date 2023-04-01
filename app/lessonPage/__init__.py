from flask import Blueprint

lessonPage = Blueprint('lessonPage', __name__)

from . import lessonList
from . import sign
from . import score
from . import report
from . import note