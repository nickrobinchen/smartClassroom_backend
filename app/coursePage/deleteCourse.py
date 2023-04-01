from flask import request
from flask import jsonify
from app import db
from app.models import Course,Manager,Teacher,CourseForTeacher
from . import coursePage

from app.auth import tokenUtils
import time 

@coursePage.route('/course/delete',methods = ['POST'])
@tokenUtils.token_required
def delete(user_id,role):

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
			
			if id is None:
				code = 202
				msg = 'parameter error'
			else:
				course = Course.query.filter_by(id = id).first()
				if course is not None:
					db.session.delete(course)
					db.session.commit()

				code = 200
				msg = 'delete course success'
	else:
		code = 201
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

