from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Student,Teacher
from . import studentPage

from app.auth import tokenUtils
import time 

@studentPage.route('/student/delete',methods = ['POST'])
@tokenUtils.token_required
def deleteStudent(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager' or role == 'teacher':
		manager = Manager.query.filter_by(id = user_id).first()
		teacher = Teacher.query.filter_by(id = user_id).first()
		if manager is None and teacher is None:
			code = 201
			msg = "none manager or teacher"
		else:
			values = request.json
			id = values.get('id')
			
			if id is None:
				code = 202
				msg = 'parameter error'
			else:
				student = Student.query.filter_by(id = id).first()
				if student is not None:
					db.session.delete(student)
					db.session.commit()

				code = 200
				msg = 'delete student success'
	else:
		code = 201
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

