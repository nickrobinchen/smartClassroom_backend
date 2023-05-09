from flask import request
from flask import jsonify
from app import db
from app.models import Manager, Student, Teacher
from . import studentPage

from app.auth import tokenUtils
import time


@studentPage.route('/student/edit', methods=['POST'])
@tokenUtils.token_required
def editStudent(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}

    if role == 'manager' or role == 'teacher' or role == 'super':
        values = request.json
        id = values.get('id')
        name = values.get('name')
        account = values.get('account')
        tel = values.get('tel')
        email = values.get('email')
        if name is None or account is None or id is None:
            code = 202
            msg = 'parameter error'
        else:
            student = Student.query.filter_by(id=id).first()
            if student is not None:
                student.name = name
                student.account = account
                student.tel = tel
                student.email = email
                db.session.add(student)
                db.session.commit()

            code = 200
            msg = 'edit teacher success'
    else:
        code = 201
        msg = 'access deny'

    json_to_send = {
        'code': code,
        'msg': msg,
        'data': data
    }

    return jsonify(json_to_send)
