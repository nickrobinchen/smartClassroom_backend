from flask import request
from flask import jsonify
from app import db
from app.models import Manager, Teacher
from . import teacherPage

from app.auth import tokenUtils
import time


@teacherPage.route('/teacher/edit', methods=['POST'])
@tokenUtils.token_required
def editTeacher(user_id, role):
    code = 205
    msg = 'unkonw error'
    data = {}

    if role == 'manager' or role == 'admin':
        values = request.json
        id = values.get('id')
        name = values.get('name')
        account = values.get('account')
        tel = values.get('tel')
        email = values.get('email')
        address = values.get('address')
        if name is None or account is None or id is None:
            code = 202
            msg = 'parameter error'
        else:
            teacher = Teacher.query.filter_by(id=id).first()
            if teacher is not None:
                teacher.name = name
                teacher.account = account
                teacher.tel = tel
                teacher.address = address
                teacher.email = email
                db.session.add(teacher)
                db.session.commit()

            code = 200
            msg = 'edit teacher success'
    else:
        code = 203
        msg = 'access deny'

    json_to_send = {
        'code': code,
        'msg': msg,
        'data': data
    }

    return jsonify(json_to_send)
