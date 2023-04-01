from flask import request
from flask import jsonify
from app import db
from app.models import Course,Manager,Teacher,CourseForTeacher
from . import teacherPage

from app.auth import tokenUtils
import time 

@teacherPage.route('/teacher/list',methods = ['GET'])
@tokenUtils.token_required
def teacherList(user_id,role):

	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager':
		manager = Manager.query.filter_by(id = user_id).first()
		if manager is None:
			code = 201
			msg = "none manager"
		else:
			teacherListDB = Teacher.query.all();
			teacherList = []
			index = 0
			for teacher in teacherListDB:
				index = index + 1
				aTeacher = {}
				aTeacher['index'] = index
				aTeacher['id'] = teacher.id
				aTeacher['name'] = teacher.name
				aTeacher['account'] = teacher.account
				aTeacher['address'] = teacher.address
				aTeacher['email'] = teacher.email
				aTeacher['tel'] = teacher.tel

				teacherList.append(aTeacher)

			data = {'items':teacherList}
			code = 200
			msg = "success"
			
	else:
		code = 202
		msg = 'access deny'

	json_to_send = {
		'code':code,
		'message':msg,
		'result':data,
		'total':len(teacherList)
	}

	return jsonify(json_to_send)

