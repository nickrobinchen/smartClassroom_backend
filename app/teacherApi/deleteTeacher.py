from flask import request
from flask import jsonify
from app import db
from app.models import Manager, Teacher
from . import teacherPage

from app.auth import tokenUtils
import time


@teacherPage.route('/teacher/delete', methods=['POST'])
@tokenUtils.token_required
def delete(user_id, role):
    code = 205
    msg = 'unkonw error'
    data = {}

    if role == 'manager' or role == 'admin':
        values = request.json
        print(values)
        id = values.get('id')

        print(id)
        if id is None:
            code = 202
            msg = 'parameter error'
        else:
            teacher = Teacher.query.filter_by(id=id).first()
            if teacher is not None:
                db.session.delete(teacher)
                db.session.commit()

            code = 200
            msg = 'delete teacher success'
    else:
        code = 203
        msg = 'access deny'

    json_to_send = {
        'code': code,
        'msg': msg,
        'data': data
    }

    print(json_to_send)
    return jsonify(json_to_send)
