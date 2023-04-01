from flask import request
from flask import jsonify
from app import db
from app.models import Course,Manager,Teacher,CourseForTeacher
from . import coursePage

from app.auth import tokenUtils
import time 

@coursePage.route('/course/edit',methods = ['POST'])
@tokenUtils.token_required
def edit(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager':
		manager = Manager.query.filter_by(id = user_id).first()
		if manager is None:
			code = 201
			msg = "none manager"
		else:
			values = request.json
			id = values.get('id')
			name = values.get('name')
			grade = values.get('grade')
			if name is None or grade is None or id is None:
				code = 202
				msg = 'parameter error'
			else:
				course = Course.query.filter_by(id = id).first()
				if course is not None:
					course.name = name
					course.grade = grade
					db.session.add(course)
					db.session.commit()

				code = 200
				msg = 'edit course success'
	else:
		code = 201
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

